from db.supabase import supabase_client

# get_num_points_for_user_id

def get_num_points_for_user_id(user_id, curr_semester):
    res1 = supabase_client.rpc(
    "get_num_deltatau_points_for_user_id",
    {"in_user_id": user_id, "in_semester": curr_semester}
    ).execute()
    return res1.data or 0  # or int(res1.data)

# leaderboard
def get_ranked_leaderboard(curr_semester):
    res1 = supabase_client.rpc(
    "get_ranked_deltatau_leaderboard",
    {"in_semester": curr_semester, "in_limit": 10}
    ).execute()
    return res1.data
    # list of dicts w/ rank, user_id, num_points

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

# get a deltatau entry by timestamp
def get_deltatau_by_ts(ts):
    res = supabase_client.table('deltatau').select('*').eq('ts', ts).execute()
    if res.data and len(res.data) > 0:
        return res.data[0]
    return None

# flag a deltatau entry
def flag_deltatau(ts):
    supabase_client.table('deltatau').update({'flagged': True}).eq('ts', ts).execute()

# unflag a deltatau entry
def unflag_deltatau(ts):
    supabase_client.table('deltatau').update({'flagged': False}).eq('ts', ts).execute()