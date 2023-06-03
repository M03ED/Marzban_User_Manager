# Marzban_User_Manager

<a href="./README-fa.md">
	فارسی
	</a>

## Features
- Multiplication Remaining Traffic For All Users
- Increase And Decrease The Same Traffic To All Users
- Increase And Decrease The Same Time From All Users
- Remove Users Depend On Expire Date

# How To Use 💡

First Enable Api In Your Marzban , 
You Can Enable It By Adding DOCS=True To Your env File

## Linux

```bash
git clone https://github.com/M03ED/Marzban_User_Manager
cd Marzban_User_Manager
wget -qO- https://bootstrap.pypa.io/get-pip.py | python3 -
python3 -m pip install -r requirements.txt
python3 main.py
```

## Windows
1. Download Project And Extract It 
2. Install Python +3.10
3. Open cmd
4. Run These Commands
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install -r requirements.txt
```
Now You Can Run Script With This Command
```
python main.py
```

# Additional Settings 🧩

If You Dont Want Enter Your Server Information You Can Replace This Lines With Your Real Information 

```bash
username = input('Enter Your Username:')
password = input('Enter Your Password:')
DOMAIN = input('Enter Your Panel Domain (without https):')
PORT = input('Enter Your Panel Port (1-65535):')
```

Example:
```bash
username = 'username'
password = 'password'
DOMAIN = 'domain.com'
PORT = '12345'
```
# Contributors
If You See A Bug Or You Have Idea To Make Script Better You Can Make Pull Request And Commit The Changes
