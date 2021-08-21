try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.uic import loadUi
except ModuleNotFoundError:
    os.system("pip install PyQt5")
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.uic import loadUi
import sys
import os
import shutil
import time

class Ui_Dialog(QDialog):
	def __init__(self, *args):
		super(Ui_Dialog, self).__init__(*args)
		loadUi(r'Resources\ShallowSeaamsupdaterpc.ui', self)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.Button.clicked.connect(self.Update)
		self.comboBox.currentTextChanged.connect(self.comboBoxRefresh)
		self.textBrowser.append('Welcome to ShallowSea-ams updater')
		global PathBool 
		PathBool = False
		self.Button.setEnabled(False)

	def move_file(self,orgin_path,moved_path):
		dir_files=os.listdir(orgin_path)            
		for file in  dir_files:
			file_path=os.path.join(orgin_path,file)  
			if os.path.isfile(file_path):          
				if os.path.exists(os.path.join(moved_path,file)):
					#print(file)
					continue
				else:
					shutil.copy(file_path, moved_path)
			if os.path.isdir(file_path):  
				path1 = os.path.join(os.path.abspath(moved_path), file)	
				if os.path.exists(path1) == False:			
					shutil.copytree(file_path,path1)
				#else:
				#	print(path1)

	def DeleteFiles(self,path,remainDirsList,fileList):
		dirsList = []
		dirsList = os.listdir(path)
		for file in dirsList:	
			if file not in remainDirsList:
				filepath = os.path.join(path,file)
				if os.path.isdir(filepath):
					#print(filepath)
					shutil.rmtree(filepath, True)			
				elif file not in fileList:
					#print(filepath)
					os.remove(filepath)

	def getDirectory(self):
		global upd_path
		upd_path = QFileDialog.getExistingDirectory(None,"Choose folder","C:/")
		if os.path.exists(upd_path+'\\atmosphere\\') == True and os.path.exists(upd_path+'\\sept\\') == True:
			self.textBrowser.append('SahllowSea-ams path ' + upd_path)
			self.textBrowser.append('Updating...Do not close this app')
			self.Button.setText('Start Update')
			global PathBool
			PathBool = True
		else:
			self.textBrowser.append('Please reselect the path of ShallowSea-ams')
	def installNew(self):

		
		path_bak =os.path.abspath(self.comboBox.currentText() + '\\SU_Bak\\')
		if not os.path.exists(path_bak):
			os.makedirs(path_bak)
		else:
			shutil.rmtree(path_bak,True)
			os.makedirs(path_bak)
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents\\0100000000001000')
		if os.path.exists(path):
			shutil.rmtree(path,True)	
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents\\0100000000001013')
		if os.path.exists(path):
			shutil.rmtree(path,True)	
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents\\0100000000001007')
		if os.path.exists(path):
			shutil.rmtree(path,True)
		path =os.path.abspath(self.comboBox.currentText()+'\\switch\\Checkpoint\\saves')
		if os.path.exists(path):		
			shutil.copytree(path, path_bak+'\\Checkpoint\\saves')
		path = self.comboBox.currentText()+'\\'
		dirsList=['Nintendo','emuMMC','SU_Bak','game save dont delete','JKSV','emuiibo','warmboot_mariko','backup','lakka','Neumann','Roms','Rom','switch','themes','retroarch','config','atmosphere file','sxos file']
		fileList=['license.dat']
		self.DeleteFiles(path,dirsList,fileList)


		global upd_path
		source = upd_path
		target = self.comboBox.currentText()+'\\'
		self.move_file(source,target)

		source = path_bak+'\\Checkpoint\\'
		target = self.comboBox.currentText()+'\\switch\\Checkpoint\\'
		if os.path.exists(source):
			self.move_file(source,target)
            
		source = path_bak+'\\pfba\\'
		target = self.comboBox.currentText()+'\\switch\\pfba\\'
		if os.path.exists(source):
			self.move_file(source,target)            

		shutil.rmtree(path_bak,True)
		self.textBrowser.append('Finished')
		reply = QMessageBox.information(self,'Finished',"Successfully update",QMessageBox.Yes,QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			os._exit(0)


	@pyqtSlot()			
	def Update(self):
		global PathBool
		if PathBool == False:
			self.getDirectory()
		else:
			self.installNew()

	@pyqtSlot()
	def comboBoxRefresh(self):
		if os.path.exists(self.comboBox.currentText()+'\\atmosphere\\') == True and os.path.exists(self.comboBox.currentText()+'\\sept\\') == True:
			self.textBrowser.append('sd card select '+self.comboBox.currentText())
			self.Button.setEnabled(True)
		else:
			self.textBrowser.append('cannot mount sd card. Please mount another one')
			self.Button.setEnabled(False)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui=Ui_Dialog()
	
	ui.show()
	sys.exit(app.exec_()) 
