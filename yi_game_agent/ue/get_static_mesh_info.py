import unreal
import json
import os

# 指定导出JSON文件的路径
OUTPUT_JSON_PATH = os.path.join(os.path.dirname(__file__), "art_assets_staticmeshes.json")

def get_static_mesh_info(mesh: unreal.StaticMesh):
    # 获取基础信息
    asset_name = mesh.get_name()
    asset_path = mesh.get_path_name()
    file_type = ".uasset"
    
    # 获取LOD和面数信息
    # Unreal中获取面数可通过MeshDescription或LOD数据实现
    # 这里以LOD 0为例（通常为最高细节LOD）
    lod_count = mesh.get_num_lods()
    polygon_count = 0
    uv_sets = 0
    
    # 尝试使用MeshDescription获取面数、UV数量
    # 对于UE5，可使用StaticMesh描述对象，如下调用会在Python中可用，但需注意引擎版本兼容性
    # 在UE Python中，一般需先获取MeshDescription对象
    # 假设使用LOD0:
    mesh_desc = unreal.StaticMeshDescription.create_static_mesh_description(mesh, lod_index=0)
    # polygon_count = mesh_desc.get_num_polygons() # 在较新版本中，可能有此接口
    # 如果没有直接方法，可以通过triangles计数获取：每个polygon一般3个triangle vertex
    
    polygon_count = mesh_desc.get_num_triangles() if hasattr(mesh_desc, 'get_num_triangles') else 0
    uv_sets = mesh_desc.get_num_uv_channels() if hasattr(mesh_desc, 'get_num_uv_channels') else 1

    # 材质信息
    materials = mesh.get_materials()
    material_slots = len(materials)
    
    # 获取材质和纹理信息（只能间接获取，每个材质可能对应多个纹理，需要解析材质实例）
    # 这里示例仅记录材质名称和路径。如需纹理分辨率，需要对材质和纹理进行进一步解析
    textures_used = []
    for mat_slot in materials:
        if mat_slot.material_interface:
            mat = mat_slot.material_interface
            mat_name = mat.get_name()
            mat_path = mat.get_path_name()
            # 深入材质解析纹理可能较复杂，这里仅做基本记录
            # 如果要更深入，需要解析Material Graph或Material Instance参数
            # 暂时留空textures_used，或写入占位信息
            # textures_used.extend(...) # 可扩展逻辑
    # 简化示例，不从材质中提取纹理信息，或者假设已知纹理(可后期扩展)
    
    technical_data = {
        "polygon_count": polygon_count,
        "material_slots": material_slots,
        "textures_used": textures_used,  # 空列表可稍后补充
        "uv_sets": uv_sets,
        "lod_levels": lod_count,
        "collision_primitives": []  # 可根据需要调用mesh.get_bounds()和collision设置
    }

    # 简单的自然语言描述(可根据资产命名规则自动生成，也可后期人工补充)
    # 这里简单地基于名称生成一段描述
    natural_language_description = f"A static mesh named {asset_name} with approximately {polygon_count} polygons. It appears to be a generic prop. Further artistic details should be provided."

    visual_description = {
        "art_style": "Unspecified",
        "color_palette": [],
        "surface_detail": "Not specified",
        "natural_language_description": natural_language_description
    }

    # 构建JSON对象
    # 为了示例简单化，一些字段留空或默认值，可后续扩展
    asset_json = {
        "asset_name": asset_name,
        "asset_type": "Static Mesh",
        "resource_path": asset_path,
        "file_type": file_type,
        "technical_data": technical_data,
        "visual_description": visual_description,
        "contextual_info": {
            "usage_context": "Unspecified",
            "associated_levels": [],
            "related_assets": [],
            "tags": []
        },
        "material_info": {
            "base_material": {},
            "material_parameters": {}
        },
        "metadata": {
            "author": "Unknown",
            "creation_date": "Unknown",
            "license_info": "Internal",
            "version": "1.0"
        },
        "screenshot_descriptions": []
    }

    return asset_json

def main():
    # 获取所有静态网格资源
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    static_mesh_assets = asset_registry.get_assets_by_path("/Game", recursive=True)
    
    # 过滤出StaticMesh资产
    static_mesh_assets = [a for a in static_mesh_assets if a.asset_class == "StaticMesh"]

    results = []

    for asset_data in static_mesh_assets:
        # 加载资产
        loaded_asset = unreal.EditorAssetLibrary.load_asset(asset_data.object_path_string)
        if isinstance(loaded_asset, unreal.StaticMesh):
            asset_json = get_static_mesh_info(loaded_asset)
            results.append(asset_json)

    # 将所有结果写入JSON文件
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"导出完成，共处理 {len(results)} 个Static Mesh资产。JSON已生成：{OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    main()
