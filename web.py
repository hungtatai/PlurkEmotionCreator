from flask import Flask, request, render_template, url_for, send_from_directory, redirect
from werkzeug import secure_filename
import pprint
from ImageSplitter import ImageSplitter
import time
import os
import hashlib

def uniqid(cls):
    
    return 

app = Flask(__name__)


app.config['FILE_PATH'] = os.path.split(os.path.realpath(__name__))[0]
app.config['UPLOAD_PATH'] = app.config['FILE_PATH'] + '\upload'
app.config['UPLOAD_TEMP_PATH'] = app.config['FILE_PATH'] + '\upload_tmp'



@app.route('/')
@app.route('/<filename>/<int:hpart>/<int:wpart>')
def index(filename = None, hpart = 0, wpart = 0):
    if filename != None and hpart in [1,2,3] and wpart in [1,2,3]:
        folder = os.path.join(app.config['UPLOAD_PATH'], filename)
        pp = pprint.PrettyPrinter(4)
        if not os.path.isdir( folder ):
            return redirect( url_for('index') )

        images = [ [ "%s_%dx%d" % (filename, i, j) for j in range(0, wpart) if os.path.exists( os.path.join(folder, "%s_%dx%d.jpg" % (filename, i, j) ) ) ] for i in range(0, hpart) ]
        images = [ l for l in images if l ] #刪掉空的list

        
        return render_template('plurk_Emotion.html', images = images)#pp.pformat(images)#render_template('plurk_Emotion.html', images = images)
    else:
        return render_template('plurk_Emotion.html')


@app.route('/uploadfile', methods = ['post'])
def uploadfile():
    msg = 'init'
    images = []
    
    try:
        hpart = int (request.form['hpart'] if request.form.has_key('hpart') and request.form['hpart'] in ['1','2','3'] else 3 )
        wpart = int (request.form['wpart'] if request.form.has_key('wpart') and request.form['wpart'] in ['1','2','3'] else 3 )
        
        
        # generate tmp file name
        m = hashlib.md5( str(time.time()) )
        tmpfilename = m.hexdigest()
        filepath = os.path.join(app.config['UPLOAD_TEMP_PATH'], tmpfilename)

        # save tmp file
        upload_imgfile = request.files['image_file']
        upload_imgfile.save(filepath)

        # split tmp file and save
        imgSplit = ImageSplitter(filepath)
        images, basename = imgSplit.split(hpart, wpart)
        imgSplit.SaveAllImage(app.config['UPLOAD_PATH'])

        #close and remove tmp file
        upload_imgfile.close()
        os.remove(filepath)
        return redirect( url_for('index', filename=basename, hpart=hpart, wpart=wpart) )
    except:
        pass
        return redirect( url_for('index') )

    '''
    html = '';
    for img in images:
        html += '<img src="%s" />' % str(url_for('image')+'/'+img['name'])
        
    return html'''
    #return pp.pformat(request.form)+pp.pformat(request.form.has_key('hpart'))+pp.pformat( request.form['hpart'] in ['1','2','3'])
    
    #return redirect( url_for('/'.join(['',basename,str(hpart),str(wpart)])) )
    #return redirect( url_for('/') )


@app.route('/image/<filename>')
def image(filename):
    filename = secure_filename(filename).split('.')[0]+'.jpg'
    folder = filename.split('_')[0]
    path = os.path.join(app.config['UPLOAD_PATH'], folder)
    if os.path.exists( os.path.join(path, filename) ):
        return send_from_directory(path, filename)
    else:
        return redirect( url_for('index') ) #render_template('Error.html', msg=u'此頁面不存在')


if __name__ == '__main__':
    #app.debug = True
    app.run(host="0.0.0.0", port=5000)
