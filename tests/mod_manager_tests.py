'''
Created on 01.06.2014

@author: Schleppi
'''
from unittest import TestCase

from d2mp.mod_manager import ModManager
from os import path
from mock import Mock
from tempfile import mkdtemp
from os.path import join, isdir, isfile, basename
import shutil, os


class FinderTest(TestCase):

    def test_singleton(self):
        man1 = ModManager()
        man2 = ModManager()
        
        self.assertEqual(man1, man2)
        
    def test_steam_and_dota_should_be_installed(self):
        steam_exe = ModManager().find_steam_exe()
        self.assertIsNotNone(steam_exe, "please install steam")
        self.assertTrue(path.exists(steam_exe), "steam executable does not exist: %s" %(steam_exe))
        self.assertTrue(path.isfile(steam_exe), "steam executable should be a file: %s" %(steam_exe))
        
        dota_exe = ModManager().find_dota_exe()
        self.assertIsNotNone(dota_exe, "please install dota!")
        self.assertTrue(path.exists(dota_exe), "dota executable does not exist: %s" %(dota_exe))
        self.assertTrue(path.isfile(dota_exe), "dota executable should be a file: %s" %(dota_exe))
        
class ModTest(TestCase):  
    
    def setUp(self):
        self.manager = ModManager()
        self.real_method = self.manager._dota_path 
        self.manager._dota_path = Mock(return_value = mkdtemp())

        self.mod1_folder = join(self.manager._d2mp_path(), "mod1")
        self.mod1_info_file = join(self.mod1_folder, "addoninfo.txt")
        
        self.mod2_folder = join(self.manager._d2mp_path(), "mod2")
        self.mod2_info_file = join(self.mod2_folder, "addoninfo.txt")
        
        
        self.mod_to_delete_folder = join(self.manager._d2mp_path(), "mod_to_delete")
        self.mod_to_delete_info_file = join(self.mod2_folder, "addoninfo.txt")
        
        self.mods = [basename(f) for f in [self.mod1_folder, self.mod2_folder]]
        
        for folder in [self.mod1_folder, self.mod2_folder, self.mod_to_delete_folder]:
            if not isdir(folder): os.mkdir(folder)
        
        for f in [self.mod1_info_file, self.mod2_info_file, self.mod_to_delete_info_file]:
            if not isfile(f): open(f, "w").close()
        
        shutil.rmtree(self.manager._mod_path())
        
    
    def tearDown(self):
        shutil.rmtree(self.manager._d2mp_path())
        self.manager._dota_path = self.real_method
    
    def test_mod_names(self):
        for mod in self.mods:
            self.assertIn(mod, self.manager.mod_list_as_string(), "mods \"%s\" was not in the mod list!" %(mod))
        
    def test_setting_mod(self):
        mod1_name, mod2_name = self.mods
        
        self.assertNotIn(mod2_name, os.listdir(self.manager._mod_path()), "mod2 should NOT be active now")
        self.assertNotIn(mod1_name, os.listdir(self.manager._mod_path()), "mod1 should NOT be active now")    
        self.manager.set_mod(mod1_name)
        self.assertIn(mod1_name, os.listdir(self.manager._mod_path()), "mod1 should be active now")
        
        self.assertNotIn(mod2_name, os.listdir(self.manager._mod_path()), "mod2 should NOT be active now")        
        self.manager.set_mod(mod2_name)
        self.assertIn(mod2_name, os.listdir(self.manager._mod_path()), "mod2 should be active now")
        self.assertNotIn(mod1_name, os.listdir(self.manager._mod_path()), "mod1 should NOT be active now")    
        
    def test_deleting_mod(self):
        mod_name = basename(self.mod_to_delete_folder)
        self.assertIn(mod_name, os.listdir(self.manager._d2mp_path()), "mod should be in d2mp folder")
        self.manager.delete_mod(mod_name)
        self.assertNotIn(mod_name, os.listdir(self.manager._d2mp_path()), "mod should NOT be in d2mp folder")
    
    def test_delete_all_mods(self):
        mod1, mod2 = self.mods
        mod3 = basename(self.mod_to_delete_folder)
        
        for mod in [mod1, mod2, mod3]:
            self.assertIn(mod, os.listdir(self.manager._d2mp_path()), "all mods should be present")
        
        self.manager.delete_mods()
        
        self.assertTrue(len(os.listdir(self.manager._d2mp_path())) == 0, "no mods should be present in d2mp folder anymore")
        self.assertTrue(len(os.listdir(self.manager._mod_path())) == 0, "no mods should be present in mod folder anymore")
        
        
    
        
        
        