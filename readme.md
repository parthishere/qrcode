first install python3 in your device
and install dependancies with: 

=> pip install -r requirements.txt

then clone the repository with :

=> git clone "https://github.com/parthishere/qrcode.git"

after cloneing it go to where manage.py file is located and just run 

=> py manage.py runserver

it will run the server on http://127.0.0.1:8000
then go to admin panel > PassModels > import and import excel sheet like i have given for example in same directory named as Book1.xlxs aster importing we can send mail to recipeints

to send email just hit enter on :
=> http://127.0.0.1:8000/email
and wait till "Email Sent!" message appears

and hola message is sent 
after recieving the qr code we can scan on scan page given in navbar 

colours of detaction gives us message:

green : Firstime entry and QR code is valid
blue: Sencond time scanning means error ! 
and red means given QR was not recognized

we can fetch the list on completed tab and uncompleted tabs ..



