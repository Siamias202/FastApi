import json
from fastapi import APIRouter,HTTPException,Request
from models.user import User
from typing import List
from auth.password_hasher import hasher
import bcrypt
user_router=APIRouter()




@user_router.get('/')
async def getallUsers()->List[User]:
    users=await User.find_all().to_list()
    if len(users)==0:
        return {"message":"No users found"}

    return users  

@user_router.post('/')
async def registration(user:User): 
    req_user=json.loads(user.json())
    if  (req_user["user_name"] and req_user["password"] and req_user["address"] and req_user["position"] and req_user["email"]):
        find_email=await User.find({"email":user.email}).to_list()
        if(len(find_email)>0):
            return {"message":"email already exists"}
        
        else:
           hashed_password= hasher.hash_the_password(user.password.encode('utf-8'))
           user.password=hashed_password
           try:
                await user.create()
                return {"message":"User created"}
           except:
                raise HTTPException(status_code=404,detail="Unable to add")  
          
           
    else:
        print(json.dumps(req_user,indent=2))
        return {"message":"Please provide all the information"}       


@user_router.post('/login')
async def user_login(user_info:Request):
    req_user_info = await user_info.json()
    print(req_user_info["password"])
    if (req_user_info["email"] and req_user_info["password"]):
        get_user = await User.find({"email":req_user_info["email"]}).to_list()
        if(len(get_user)==1):
            is_match=bcrypt.checkpw(req_user_info["password"],get_user["password"])
            if(is_match):
                return {"message":"Ok valid user"}
            else:
                return {"message":"Password wrong"}    
        else:
            return {"message":"No User found"}
        


    else:
        return {"message":"Please fill all the fields"}
    

   
    



