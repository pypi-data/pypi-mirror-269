import struct
from io import BytesIO
from typing import Any, Union

import numpy as np
import shapefile
import shapely.geometry as sgeom

from frykit.help import PathType

'''
利用类似NetCDF的有损压缩方式, 将64-bit的shapefile转换成32-bit的整数.
高德地图数据的精度为1e-6, 压缩参数能保证1e-7的精度. 应该够用了吧...?
'''

PolygonType = Union[sgeom.Polygon, sgeom.MultiPolygon]

# 几何类型.
POLYGON_TYPE = 0
MULTI_POLYGON_TYPE = 1

# 数据类型.
DTYPE = '<I'
DTYPE_SIZE = 4

# 压缩参数.
LON0, LON1 = -180, 180
LAT0, LAT1 = -90, 90
N = DTYPE_SIZE * 8
ADD_OFFSETS = np.array([LON0, LAT0])
SCALE_FACTORS = np.array([LON1 - LON0, LAT1 - LAT0]) / (2**N - 1)


class BinaryConverter:
    '''将shapefile文件转为二进制的类.'''

    def convert(self, filepath: PathType) -> None:
        '''转换filepath指向的文件.'''
        with shapefile.Reader(str(filepath)) as reader:
            if reader.shapeType != 5:
                raise ValueError('shp文件必须是Polygon类型')
            geojson = reader.__geo_interface__

        return self.pack_geojson(geojson)

    def pack_geojson(self, geojson: dict) -> bytes:
        '''将GeoJSON对象打包成二进制.'''
        shapes = []
        shape_sizes = []
        for feature in geojson['features']:
            geometry = feature['geometry']
            if geometry['type'] == 'Polygon':
                shape = self.pack_polygon(geometry['coordinates'])
                shape_type = struct.pack(DTYPE, POLYGON_TYPE)
            elif geometry['type'] == 'MultiPolygon':
                shape = self.pack_multi_polygon(geometry['coordinates'])
                shape_type = struct.pack(DTYPE, MULTI_POLYGON_TYPE)
            else:
                raise ValueError('不支持的几何类型')
            shape = shape_type + shape
            shape_sizes.append(len(shape))
            shapes.append(shape)

        shapes = b''.join(shapes)
        num_shapes = struct.pack(DTYPE, len(shape_sizes))
        shape_sizes = np.array(shape_sizes, DTYPE).tobytes()
        content = b''.join([num_shapes, shape_sizes, shapes])

        return content

    def pack_polygon(self, coordinates: list) -> bytes:
        '''将Polygon的坐标打包成二进制.'''
        rings = []
        ring_sizes = []
        for coords in coordinates:
            coords = np.array(coords)
            coords = np.round((coords - ADD_OFFSETS) / SCALE_FACTORS)
            ring = coords.astype(DTYPE).tobytes()
            ring_sizes.append(len(ring))
            rings.append(ring)

        rings = b''.join(rings)
        num_rings = struct.pack(DTYPE, len(ring_sizes))
        ring_sizes = np.array(ring_sizes, DTYPE).tobytes()
        polygon = b''.join([num_rings, ring_sizes, rings])

        return polygon

    def pack_multi_polygon(self, coordinates: list) -> bytes:
        '''将MultiPolygon的坐标打包成二进制.'''
        polygons = list(map(self.pack_polygon, coordinates))
        polygon_sizes = list(map(len, polygons))

        polygons = b''.join(polygons)
        num_polygons = struct.pack(DTYPE, len(polygon_sizes))
        polygon_sizes = np.array(polygon_sizes, DTYPE).tobytes()
        multi_polygon = b''.join([num_polygons, polygon_sizes, polygons])

        return multi_polygon


class BinaryReader:
    '''读取二进制文件的类.'''

    def __init__(self, filepath: PathType) -> None:
        self.file = open(str(filepath), 'rb')
        self.num_shapes = struct.unpack(DTYPE, self.file.read(DTYPE_SIZE))[0]
        self.shape_sizes = np.frombuffer(
            self.file.read(self.num_shapes * DTYPE_SIZE), DTYPE
        )
        self.header_size = self.file.tell()
        self.shape_offsets = (
            self.shape_sizes.cumsum() - self.shape_sizes + self.header_size
        )

    def close(self) -> None:
        self.file.close()

    def __enter__(self) -> None:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def shape(self, i: int = 0) -> PolygonType:
        '''读取第i个几何对象.'''
        if i >= self.num_shapes:
            raise ValueError(f'i应该小于{self.num_shapes}')

        self.file.seek(self.shape_offsets[i])
        buffer = BytesIO(self.file.read(self.shape_sizes[i]))
        shape_type = struct.unpack(DTYPE, buffer.read(DTYPE_SIZE))[0]
        if shape_type == POLYGON_TYPE:
            return self.unpack_polygon(buffer)
        elif shape_type == MULTI_POLYGON_TYPE:
            return self.unpack_multi_polygon(buffer)
        else:
            raise RuntimeError('不支持的几何类型')

    def shapes(self) -> list[PolygonType]:
        '''读取所有几何对象.'''
        shapes = []
        self.file.seek(self.header_size)
        for shape_size in self.shape_sizes:
            buffer = BytesIO(self.file.read(shape_size))
            shape_type = struct.unpack(DTYPE, buffer.read(DTYPE_SIZE))[0]
            if shape_type == POLYGON_TYPE:
                shape = self.unpack_polygon(buffer)
            elif shape_type == MULTI_POLYGON_TYPE:
                shape = self.unpack_multi_polygon(buffer)
            else:
                raise RuntimeError('不支持的几何类型')
            shapes.append(shape)

        return shapes

    def unpack_polygon(self, buffer: BytesIO) -> sgeom.Polygon:
        '''将Polygon的二进制解包为几何对象.'''
        num_rings = struct.unpack(DTYPE, buffer.read(DTYPE_SIZE))[0]
        ring_sizes = np.frombuffer(buffer.read(num_rings * DTYPE_SIZE), DTYPE)

        rings = []
        for ring_size in ring_sizes:
            ring = np.frombuffer(buffer.read(ring_size), DTYPE).reshape(-1, 2)
            ring = ring * SCALE_FACTORS + ADD_OFFSETS
            rings.append(ring)
        polygon = sgeom.Polygon(rings[0], rings[1:])

        return polygon

    def unpack_multi_polygon(self, buffer: BytesIO) -> sgeom.MultiPolygon:
        '''将MultiPolygon的二进制解包为几何对象.'''
        num_polygons = struct.unpack(DTYPE, buffer.read(DTYPE_SIZE))[0]
        polygon_sizes = np.frombuffer(
            buffer.read(num_polygons * DTYPE_SIZE), DTYPE
        )

        polygons = []
        for polygon_size in polygon_sizes:
            buffer_ = BytesIO(buffer.read(polygon_size))
            polygon = self.unpack_polygon(buffer_)
            polygons.append(polygon)
        multi_polygon = sgeom.MultiPolygon(polygons)

        return multi_polygon
