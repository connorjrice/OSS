create table [if not exists] [peak].clients(
    name text,
    username text,
    member_id integer,
    phone_number text,
    address text,
    email text primary key,
    total_income integer
    
)

create table [if not exists] peak.user_tracking(
   member_id integer,
   datetime text,
   timezone text
)

create table [if not exists] peak.users(
   user_name text,
   bhash text
)
