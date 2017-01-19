with recursive
     cte(id, reply_id, reply_to_id, rdr_message, rdr_name, message_date) as (
     select id, reply_id, reply_to_id, rdr_message, rdr_name ,message_date from Comment where reply_id = 'fa102480-dd21-11e6-b1ae-f4066974556c' and approved = 1 and uid = '3928f38e-d702-11e6-94'
     union all
     select Comment.id, Comment.reply_id, Comment.reply_to_id, Comment.rdr_message, Comment.rdr_name, Comment.message_date from Comment join cte on Comment.reply_id = cte.reply_to_id
     )
select * from cte
     