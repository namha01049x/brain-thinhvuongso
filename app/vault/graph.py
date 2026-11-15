from typing import Dict, Any, List
from app.vault.reader import get_all_notes

def get_cluster_name(folder: str, tags: List[str]) -> str:
    """Xác định cụm chủ đề của note để tô màu trên đồ thị 3D."""
    folder_lower = folder.lower()
    tag_str = " ".join(tags).lower()

    if "04" in folder_lower or "marketing" in folder_lower or "ad" in tag_str or "facebook" in tag_str:
        return "MARKETING & ADS"
    elif "03" in folder_lower or "work" in folder_lower or "project" in folder_lower:
        return "PROJECTS"
    elif "digital" in tag_str or "product" in tag_str or "offer" in tag_str:
        return "DIGITAL PRODUCTS"
    elif "05" in folder_lower or "knowledge" in folder_lower or "wiki" in folder_lower:
        return "WIKI & KNOWLEDGE"
    elif "02" in folder_lower or "identity" in folder_lower or "principle" in tag_str:
        return "IDENTITY & CORE"
    elif "01" in folder_lower or "inbox" in folder_lower:
        return "INBOX & IDEAS"
    elif "07" in folder_lower or "learning" in folder_lower or "book" in tag_str:
        return "LEARNING"
    else:
        return "FACTS & GENERAL"

def generate_graph_data() -> Dict[str, Any]:
    """Sinh dữ liệu đỉnh (Nodes) và cạnh (Links) tương thích thư viện 3D Force Graph."""
    notes = get_all_notes()
    
    # Map tiêu đề hoặc stem sang note id
    title_to_id = {}
    for n in notes:
        title_to_id[n["title"].lower()] = n["id"]
        title_to_id[n["filename"].lower()] = n["id"]
        title_to_id[n["filename"].replace(".md", "").lower()] = n["id"]

    nodes = []
    links = []
    link_counts = {n["id"]: 0 for n in notes}

    # Đếm số liên kết
    for n in notes:
        for target_title in n["wikilinks"]:
            target_id = title_to_id.get(target_title.lower())
            if target_id and target_id != n["id"]:
                links.append({
                    "source": n["id"],
                    "target": target_id
                })
                link_counts[n["id"]] += 1
                link_counts[target_id] += 1

    # Tạo danh sách Nodes
    cluster_stats = {}
    for n in notes:
        cluster = get_cluster_name(n["folder"], n["tags"])
        cluster_stats[cluster] = cluster_stats.get(cluster, 0) + 1
        
        # Kích thước node tỷ lệ thuận với số liên kết kết nối
        degree = link_counts.get(n["id"], 0)
        nodes.append({
            "id": n["id"],
            "name": n["title"],
            "path": n["path"],
            "folder": n["folder"],
            "cluster": cluster,
            "tags": n["tags"],
            "val": max(2, min(degree * 2 + 2, 20)),
            "degree": degree
        })

    return {
        "nodes": nodes,
        "links": links,
        "stats": {
            "total_notes": len(nodes),
            "total_links": len(links),
            "clusters": cluster_stats
        }
    }
