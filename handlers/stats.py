from app import app 
from utils.utils import get_name_from_user_id, get_num_spots_for_user_id, find_rank_by_user_id
@app.message("diversabot stats")
def post_stats(message, client):
    user_id = message["user"]
    channel_id = message["channel"]

    message_text_1: str
    message_text_2: str

    if (num_spots := get_num_spots_for_user_id(user_id, SEMESTER_ID, engine)) == 0:
        message_text_1 = f"You have not spotted anyone yet :( Go get out there!"
    else:
        rank = find_rank_by_user_id(user_id, SEMESTER_ID, engine)
        message_text_1 = f"You have spotted {num_spots} people and are currently ranked #{rank} on the leaderboard!"

    with Session(engine) as session:
        times_spotted = session.query(DiversaSpot) \
                       .filter(
                           DiversaSpot.tagged.any(user_id),
                           DiversaSpot.semester==SEMESTER_ID,
                           DiversaSpot.flagged==False) \
                       .count()
        
        if times_spotted == 0:
             message_text_2 = ":camera_with_flash: No one has spotted you yet ... so sneaky of you!"
        else:
            top_spotter_id, top_spotter_num_spots = session.query(
                            DiversaSpot.spotter, 
                            sqlalchemy.func.count(DiversaSpot.spotter).label('spot_count')
                        ) \
                        .filter(DiversaSpot.tagged.any(user_id), DiversaSpot.flagged==False) \
                        .group_by(DiversaSpot.spotter) \
                        .order_by(sqlalchemy.desc('spot_count')) \
                        .first()
            message_text_2 = f":camera_with_flash: You've been spotted a total of {num_spots} " + \
            f"times!\n\n:heart_eyes: *{get_name_from_user_id(top_spotter_id, app)}* has spotted you " + \
            f"the most with {top_spotter_num_spots} spots."
    
    blocks = stat_blocks(date.today(), get_name_from_user_id(user_id, app), message_text_1, message_text_2)
    
    client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text="Displaying personal stat information."
    )
