import h5py
import numpy as np

# class for accessing data of stored HDF5 file this is from the limr program by andrin doll
class HDF():
    
    def __init__(self, filename = ''):
        
        # check first for the filename provided
        if filename != '':
            self.HDFsrc = filename
        else:
            self.HDFsrc = ''
        
        # get data
        self.__get_data()
        
    # just an alias for __init__ that does load a specific file
    def load(self, filename = ''):
        self.__init__(filename)
            
    # gets the data of the file        
    def __get_data(self):
        
        if (self.HDFsrc == '') | (self.HDFsrc == []):
            # initialize all as empty
            self.tdy = []
            self.tdx = []
            self.attrs = []
            self.parsoutp = {}
            self.parvar = {}
            
        else:
            f = h5py.File(self.HDFsrc, 'r')
            
            HDFkeys = list(f.keys())
            
            for ii, HDFkey in enumerate(HDFkeys):
                if ii == 0:
                    # initialize data array
                    dsize = f[HDFkey].shape
                    inddim = dsize[0]
                    self.tdy = np.zeros((int(dsize[1]/2), int(dsize[0] * len(HDFkeys))),dtype=np.complex_)
                    
                    # initialize the output objects
                    self.attrs = [dynclass() for jj in range(len(HDFkeys))]
                    
                    # get the attribute keys
                    self.parsoutp = {}
                    ii_oupargs = 0
                    for item in f[HDFkey].attrs.items():
                        itemname = item[0][5:]
                        itemarg = item[0][1:4]
                        if not ('///' in itemarg):
                            self.parsoutp[itemarg] = [ item[1], itemname]
                        else:
                            self.parsoutp['//'+str(ii_oupargs)] = [ item[1], itemname]
                            ii_oupargs+=1

                    # look for eventual parvar lists
                    self.parvar = {}
                    for item in f.attrs.items():
                        self.parvar[item[0]] = item[1]
                    
                
                # Get the data
                data_raw = np.array(f[HDFkey])
                try:
                    self.tdy[:,ii*inddim:(ii+1)*inddim] = np.transpose(np.float_(data_raw[:,::2])) + 1j*np.transpose(np.float_(data_raw[:,1::2]))
                except:
                    pass
                    
                    
                # Get the arguments
                ii_oupargs = 0  
                for item in f[HDFkey].attrs.items():
                    itemname = item[0][5:]
                    itemarg = item[0][1:4]
                    if not ('///' in itemarg):
                        setattr(self.attrs[ii], itemarg, item[1])
                    else:
                        setattr(self.attrs[ii], '//'+str(ii_oupargs), item[1])
                        ii_oupargs+=1
            
            f.close()
            srate_MHz = getattr(self.attrs[0], 'sra')*1e-6
            self.tdx = 1/srate_MHz*np.arange(self.tdy.shape[0])

    # get an argument by matching the text description
    def attr_by_txt(self, pattern):
        for key in sorted(self.parsoutp):
            if pattern in self.parsoutp[key][1]: # pattern match
                attr = getattr(self.attrs[0], key)
                try:
                    ouparr = np.zeros( ( len(attr), len(self.attrs)), attr.dtype)
                except:
                    ouparr = np.zeros( ( 1, len(self.attrs)), attr.dtype)
                    
                for ii in np.arange(len(self.attrs)):
                    ouparr[:,ii] = getattr(self.attrs[ii], key)
                return np.transpose(ouparr)
        
        print('Problem obtaining the attribute from the description using the pattern ' + pattern + '!')
        print('Valid descriptions are: ')
        self.print_params()
        
    # get an argument by key
    def attr_by_key(self, key):
        if key in dir(self.attrs[0]):
            attr = getattr(self.attrs[0], key)
            try:
                ouparr = np.zeros( ( len(attr), len(self.attrs)), attr.dtype)
            except:
                ouparr = np.zeros( ( 1, len(self.attrs)), attr.dtype)
            for ii in np.arange(len(self.attrs)):
                ouparr[:,ii] = getattr(self.attrs[ii], key)
            return np.transpose(ouparr)
        
        print('Problem obtaining the attribute from key ' + key + '!')
        print('Valid keys are: ')
        self.print_params()
               

    # print the arguments
    def print_params(self, ouponly = False):
        for key in sorted(self.parsoutp):
            val = getattr(self.attrs[0], key)
            if not('//' in key):    # input argument?
                if ouponly: continue;
                    
            print('{:<5}: {:>50}    {:<25}'.format(key, val, self.parsoutp[key][1]))
            
# empty class to store dynamic attributes, basically for the attributes in HDF keys
class dynclass:
    pass