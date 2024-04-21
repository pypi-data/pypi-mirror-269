import os,requests

class BluesFiler:
  
  @classmethod
  def removedirs(cls,directory):
    '''
    @description Remove all child dir and files
    @param {string} directory 
    '''
    for root, dirs, files in os.walk(directory):
      for file in files:
        os.remove(os.path.join(root, file))
      for dir in dirs:
        os.rmdir(os.path.join(root, dir))

  @classmethod
  def download(cls,urls,directory,success=None,error=None):
    '''
    @description Download multi files
    @param {list} urls files' remote url
    @param {string} directory : Local directory to save the downloaded files
    @param {function} success : Callback function called on success
    @param {function} error : Callback function called on failure
    @returns {dict} complex result
    '''

    result = cls.__get_result()

    if not urls:
      return result 

    for url in urls:
      # download the image
      (code,file_or_msg) = cls.download_one(url,directory)
      if code == 200:
        item = {
          'url':url,
          'file':file_or_msg,
          'callback_value':None
        }
        if success:
          item['callback_value'] = success(file_or_msg)
        result['success']['count']+=1
        result['success']['files'].append(item)
        result['files'].append(file_or_msg)
        result['code'] = 200
      else:
        item = {
          'url':url,
          'message':file_or_msg,
          'callback_value':None
        }
        if error:
          item['callback_value'] = error(str(e))
        result['error']['count']+=1
        result['error']['files'].append(item)
    
    return result 

  @classmethod
  def download_one(cls,url,directory):
    '''
    @description : download one file
    @param {str} url : file's remote url
    @param {str} directory : The dir to save the download file
    '''
    try:
      # Ensure directory existence
      cls.makedirs(directory)
      # Keep the file name unchanged
      file_name = url.split('/')[-1]
      local_file = directory+'/'+file_name

      # 永远保持覆盖
      res=requests.get(url)
      res.raise_for_status()
      with open(local_file,'wb') as f:
        f.write(res.content)
        f.close()
        return (200,local_file) 

    except Exception as e:
      return (500,str(e))

  @classmethod
  def __get_result(cls):
    return {
      'code':500,
      'files':[],
      'success':{
        'count':0,
        'files':[],
      },
      'error':{
        'count':0,
        'files':[],
      },
    }

  @classmethod
  def write(cls,file,text,mode='w'):
    '''
    @description : write text to file
    @param {str} file : file's path
    @param {str} text : content
    @param {str} mode : write mode
      - 'w' : clear the history content
      - 'a' : append text
    @returns {None} 
    '''
    with open(file,mode,encoding='utf-8') as file:
      file.write(text)

  @classmethod
  def exists(cls,path):
    '''
    @description : Does a dir or file exist
    @param {str} path
    @returns {bool} 
    '''
    return os.path.exists(path)

  @classmethod
  def makedirs(cls,path):
    '''
    @description : Create dirs (support multilevel directory) if they don't exist
    @param {str} path : multilevel dir
    @returns {None}
    '''
    if not cls.exists(path):
      os.makedirs(path)

  @classmethod
  def get_rename_file(cls,file_path,new_name='',prefix='',suffix='',separator='-'):
    '''
    @description : get the new file name path
    '''
    path_slices = file_path.split('/')
    original_name = path_slices[-1]
    copy_name = new_name if new_name else original_name
    if prefix:
      copy_name = prefix+separator+copy_name
    if suffix:
      copy_name = copy_name+separator+suffix
    path_slices[-1]=copy_name
    copy_path='/'.join(path_slices)
    return copy_path