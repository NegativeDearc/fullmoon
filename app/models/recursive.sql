with recursive
     cte(id, reply_id, reply_to_id, rdr_message, rdr_name, message_date) as (
     select id, reply_id, reply_to_id, rdr_message, rdr_name ,message_date from Comment where reply_id = '0b2b741e-dbcb-11e6-a466-f4066974556c'
     union all
     select Comment.id, Comment.reply_id, Comment.reply_to_id, Comment.rdr_message, Comment.rdr_name, Comment.message_date from Comment join cte on Comment.reply_to_id = cte.reply_id
     )
select * from cte
     