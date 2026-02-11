from db.supabase import supabase_client

# get_num_points_for_user_id

def get_num_points_for_user_id(user_id, curr_semester):
    res = supabase_client.table('deltatau') \
        .select('points') \
        .eq('new_mem', user_id) \
        .eq('semester', curr_semester) \
        .eq('flagged', False) \
        .execute()
    return sum(row['points'] for row in res.data) if res.data else 0

# leaderboard
def get_ranked_leaderboard(curr_semester):
    res = supabase_client.table('deltatau') \
        .select('new_mem, points') \
        .eq('semester', curr_semester) \
        .eq('flagged', False) \
        .execute()
    # aggregate points per user
    totals = {}
    for row in (res.data or []):
        uid = row['new_mem']
        totals[uid] = totals.get(uid, 0) + row['points']
    # sort descending and take top 10
    sorted_users = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:10]
    return [
        {'rank': i + 1, 'user_id': uid, 'num_points': pts}
        for i, (uid, pts) in enumerate(sorted_users)
    ]

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