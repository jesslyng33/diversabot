from supabase import supabase_client


# get_num_spots_for_user_id
def get_num_spots_for_user_id(user_id, curr_semester): 
    res = supabase_client.rpc(
        "get_num_spots_for_user_id", 
        {"in_user_id": user_id, "in_semester": curr_semester}).execute()
    return res.data  # int

# iter_leaderboard
def get_ranked_leaderboard(curr_semester):
    res = supabase_client.rpc(
        "get_ranked_leaderboard",
        {"in_semester": curr_semester, "in_limit": 10}
    ).execute()
    return res.data  # list of dicts with rank, user_id, num_spots

# insert diversaspot into db 
def insert_diversaspot(timestamp, spotter, tagged, semester, flagged=False): 
    # insert logic for auto flagging # 
    supabase_client.table('diversaspots').insert({timestamp, spotter, tagged, semester, flagged}).execute()
