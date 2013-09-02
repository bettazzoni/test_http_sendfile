import httplib, base64

LOCAL_FILENAME = "/sdcard/aaa.3gp"
DESTNAME = 'aaa.3gp'
DESTURL = '192.168.1.101:8080'

def send_file_via_put_http(source_file, dest_file=DESTNAME, url=DESTURL):
	h =  httplib.HTTPConnection(url)
	f = open(source_file, 'rb')
	source_bin_content = f.read()
	f.close()
	h.request(method='PUT', 
		  url=dest_file, 
		  body=base64.b64encode(source_bin_content), 
		  headers={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" } )
	return h.getresponse().read()

from androidhelper import Android

droid=Android()
def confirmDialog(title, text, positive, negative=None):
    droid.dialogDismiss()
    droid.dialogCreateAlert(title,text)
    droid.dialogSetPositiveButtonText(positive)
    if negative is not None: droid.dialogSetNegativeButtonText(negative)
    droid.dialogShow()
	# blocked until press
    response=droid.dialogGetResponse().result
    droid.dialogDismiss()
    return "positive" == (response["which"] if response.has_key("which") else "canceled" )


from jnius import autoclass
MediaRecorder= autoclass('android.media.MediaRecorder')
AudioSource  = autoclass('android.media.MediaRecorder$AudioSource')
OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

# Record the Microphone with a 3GP recorder
mRecorder = MediaRecorder()
mRecorder.setAudioSource(AudioSource.MIC)
mRecorder.setOutputFormat(OutputFormat.THREE_GPP)
mRecorder.setOutputFile(LOCAL_FILENAME)    
mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)
mRecorder.prepare()

if confirmDialog("Ready to recording to %s"%LOCAL_FILENAME, "Strart record or Cancel", "Start", "Cancel") :
	mRecorder.start()
	confirmDialog("Recording to %s"%LOCAL_FILENAME,"press SEND to stop recording and send the file","SEND")
	mRecorder.stop()
 	answ = send_file_via_put_http(LOCAL_FILENAME)
	print answ
	


