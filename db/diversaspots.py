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
    supabase_client.table('diversaspots').insert(
        {timestamp, 
         spotter, 
         tagged, 
         semester, 
         flagged}
         ).execute()

# finds rank for the specific user_id
def find_rank_by_user_id(user_id, curr_semester): 
    res = supabase_client.rpc("find_rank_by_user_id", 
                              {"in_semester": curr_semester, 
                               "in_user_id": user_id}
                               ).execute()
    return res.data or 0 

# gets times a user was spotted 
def get_times_spotted(user_id, curr_semester): 
    res = supabase_client.rpc("get_times_spotted", 
                              {"in_semester": curr_semester, 
                               "in_user_id": user_id}
                               ).execute()
    return res.data or 0 

# gets top spotter of the person that posted the message 
def get_top_spotter(user_id: str, curr_semester: str) -> tuple[str | None, int]:
    res = supabase_client.rpc(
        "get_top_spotter",
        {"in_semester": curr_semester, "in_user_id": user_id}
    ).execute()

    if not res.data:  # no one has spotted them
        return None, 0

    row = res.data[0]
    return row["spotter"], row["spot_count"]
