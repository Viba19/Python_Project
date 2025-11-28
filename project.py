import sqlite3 as sq
conn=sq.connect('project.db')
cursor=conn.cursor()
# table="""
# create table customer
# (
# cid integer primary key AutoIncrement,
# cname text not null,
# password text not null,
# pin integer not null,
# balance int not null
# )
# """
# cursor.execute(table)



import streamlit as st
menu=['signup','login']
option=st.selectbox('select the operation:',menu)

if 'logged' not in st.session_state:
    st.session_state.logged=False
    st.session_state.user=''



def deposit(u_n):
    pin=st.number_input('enter your pin:',min_value=0)
    amount=st.number_input('enter the amount:',min_value=0)
    deposit=st.button('deposit',type='primary')
    if deposit:
        query="select pin from customer where cname=?"
        cursor.execute(query,(u_n,))
        database_pin=cursor.fetchall()[0][0]
        if pin ==database_pin:
            query ="update customer set balance=balance + ? where cname= ?"
            cursor.execute(query,(amount,u_n))
            conn.commit()


def login():
    u_n=st.text_input('enter user_name:')
    password=st.text_input('enter password:')
    login=st.button('login',type='primary')
    if login:
        query="select password from customer where cname=?"
        cursor.execute(query,(u_n,))
        database_password=cursor.fetchall()[0][0]
        if password==database_password:
            st.session_state.logged=True
            st.session_state.user=u_n
        else:
            st.warning('login fail')




def password_validation(password):
    u_count=0
    l_count=0
    s_count=0
    n_count=0
    if len(password)>=8:
        for i in password:
            if i.isupper():
                u_count +=1
            elif i.islower():
                l_count +=1
            elif i.isdigit():
                n_count +=1
            else:
                s_count +=1
        if u_count>0 and l_count>0 and n_count>0 and s_count>0:
            return True
        else:
            return False
    else:
        return False


def user_name_validation(name):
    query="select cname from customer"
    cursor.execute(query)
    data=cursor.fetchall()
    for i in data:
        if name==i[0]:
            return False
    else:
        return True


def signup():
    name=st.text_input('enter your name:')
    password=st.text_input('enter your password:')
    c_p=st.text_input('enter your password again:')
    pin=st.number_input('enter your pin:',min_value=1000,max_value=9999)
    c_pin=st.number_input('enter your pin again:',min_value=1000,max_value=9999)
    amount=st.number_input('enter the amount:',min_value=500)
    submit=st.button('create',type='primary')
    if submit:
        if password==c_p and pin ==c_pin:
            p=password_validation(password) #FUNCTION
            u=user_name_validation(name) #FUNCTION
            if u:
                if p:
                    query="insert into customer (cname,password,pin,balance) values(?,?,?,?) "
                    cursor.execute(query,(name,password,pin,amount))
                    conn.commit()
                    st.success('ACCOUNT CREATED..')
                    st.balloons()
                else:
                    st.warning('password is not matching the requirement')
            else:
                st.warning('user name already exist')

if option=='signup':
    signup()
else:
    login()


def withdraw(user):
    pin=st.number_input('enter your pin:',min_value=0)
    amount=st.number_input('enter your amount',min_value=0)
    withdraw=st.button('withdraw',type='primary')
    if withdraw:
        query ="select pin,balance from customer where cname=?"
        cursor.execute(query,(user,))
        database=cursor.fetchall()[0]
        if database[0]==pin:
            if amount<=database[1]:
                query="update customer set balance =balance - ? where cname=?"
                cursor.execute(query,(amount,user))
                conn.commit()
            else:
                st.error('low balance')


def balance_check(user):
    pin = st.number_input('enter your pin:', min_value=0)
    balance = st.button('show balance', type='primary')
    if balance:
        query = "select pin,balance from customer where cname=?"
        cursor.execute(query, (user,))
        database = cursor.fetchall()[0]
        if pin == database[0]:
            st.success(f'hey {user} your account is having {database[1]} RS')

if st.session_state.logged:
    operation = ['deposit', 'withdraw', 'balance check']
    work = st.radio('choose the option', operation)
    if work == 'deposit':
        deposit(st.session_state.user)
    elif work=='withdraw':
        withdraw(st.session_state.user)
    else:
        balance_check(st.session_state.user)

