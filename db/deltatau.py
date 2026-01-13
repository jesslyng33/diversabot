from db.supabase import supabase_client

# get_num_points_for_user_id

def get_num_points_for_user_id(user_id, curr_semester):
    res1 = supabase_client.rpc(
        "get_num_points_for_user_id",
        {"in_user_id": user_id, "in_semester": curr_semester}).execute()
    return sum(res1.data) # int
    # is this legal lol

# leaderboard
def get_ranked_leaderboard(curr_semester):
    res1 = supabase_client.rpc(
    "get_ranked_leaderboard",
    {"in_semester": curr_semester, "in_limit": 10}
    ).execute()
    return res1.data # list of dicts w/ rank, user_id, num_points

# insert newmem challenge into db
def insert_deltatau(ts, new_mem, points, semester, flagged=False):
    # adding row per entry #
    supabase_client.table('deltatau').insert({
    'ts': ts,
    'new_mem': new_mem,
    'points': points,
    'semester': semester,
    'flagged': flagged
    }).execute()