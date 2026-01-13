from db.supabase import supabase_client

def get_num_points_for_user_id(user_id, curr_semester):
    res = supabase_client.rpc(
        "get_num_numbergame_points_for_user_id",
        {"in_user_id": user_id, "in_semester": curr_semester}
    ).execute()
    return sum(res.data)

def get_ranked_leaderboard(curr_semester):
    res = supabase_client.rpc(
        "get_ranked_numbergame_leaderboard",
        {"in_semester": curr_semester, "in_limit": 10}
    ).execute()
    return res.data

def insert_numbergame(ts, user_id, points, semester, flagged=False):
    supabase_client.table("numbergame").insert({
        "ts": ts,
        "user_id": user_id,
        "points": points,
        "semester": semester,
        "flagged": flagged
    }).execute()