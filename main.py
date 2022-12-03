#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Run Editor """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '19.11.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'


from EditorUI import EditorUI


text_editor = EditorUI()
text_editor.run()
