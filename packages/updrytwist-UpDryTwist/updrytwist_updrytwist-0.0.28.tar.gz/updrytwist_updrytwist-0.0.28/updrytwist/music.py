
import pygame
import logging
import datetime
import ctypes

_LOGGER = logging.getLogger(__name__)
VERSION = pygame.version.vernum

BUFFER_SIZE=4096

class Music:

    def __init__ ( self, musicFile : str, targetVolume : int ):

        self.musicFile     = musicFile
        self.hasMusic      = False
        self.targetVolume  = targetVolume
        self.fadeInSecs    = 0
        self.startTime     = datetime.datetime.now()
        self.currentVolume = -1

        try:
            pygame.mixer.pre_init(buffer=4096)
        except NotImplementedError:
            _LOGGER.debug("Music Pygame Mixer doesn't support pre-init (earlier version)")

        pygame.init()

        try:
            (major, minor, patch) = pygame.mixer.get_sdl_mixer_version()
            _LOGGER.info( f"PyGame mixer SDL version: {major}.{minor}.{patch}")
        except NotImplementedError:
            _LOGGER.debug( "Music Pygame Mixer probably not present" )

        self.trapErrors()

    @staticmethod
    def errorHandler( inFile, line, function, err, fmt ) :
        _LOGGER.info( f"Received ALSA error {inFile} line {line} function {function} error {err}")


    def trapErrors ( self ):
        try:
            ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
            c_error_handler = ERROR_HANDLER_FUNC(self.errorHandler)
            asound = ctypes.cdll.LoadLibrary('libasound.so.2')
            asound.snd_lib_error_set_handler( c_error_handler )
        except OSError as e:
            _LOGGER.info( "Received exception {e} while attempting to set the libasound.so.2 error handler.")

    def loadMusic ( self ):
        # give myself a large buffer, as well (last value), otherwise playback stutters
        # pygame.mixer.init(44100, -16, True, 4096)
        pygame.mixer.init()
        pygame.mixer.music.load( self.musicFile )
        self.hasMusic = True

    @staticmethod
    def getVolume (  ) -> int:
        return int(pygame.mixer.music.get_volume() * 100)

    def setVolume ( self, volume=None ):
        if volume:
            if volume < 0:
                volume = 0
            if volume > 99:
                volume = 99
            self.targetVolume = volume
        pygame.mixer.music.set_volume( float(self.targetVolume / 100.0) )
        self.currentVolume = self.targetVolume

    def setFadeVolume ( self ):
        now = datetime.datetime.now()
        delta = (now - self.startTime).total_seconds()
        if delta >= self.fadeInSecs:
            volume = self.targetVolume
        else:
            volume = int(self.targetVolume * delta / self.fadeInSecs)
        if volume != self.currentVolume:
            pygame.mixer.music.set_volume( float(volume / 100.0) )
            self.currentVolume = volume

    def unloadMusic ( self ):
        try:
            self.hasMusic = False
            if pygame.mixer.music and VERSION[0] >= 2:
                pygame.mixer.music.unload()
            if pygame.mixer and pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception as e:
            _LOGGER.info( f'Got exception when attempting to unload music: {e}', exc_info=True)

    def playMusic ( self, nbrRepetitions : int = 0, fadeSeconds : int = 0 ):
        if not self.hasMusic:
            self.loadMusic()
        self.startTime     = datetime.datetime.now()
        self.fadeInSecs    = fadeSeconds
        self.currentVolume = -1
        pygame.mixer.music.play( loops=nbrRepetitions-1 )
        self.setFadeVolume()

    def stopMusic ( self ):
        try:
            self.currentVolume = -1
            if pygame.mixer.get_busy() and pygame.mixer.music and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.stop()
        except Exception as e:
            _LOGGER.info( f'Got exception when attempting to stop music: {e}', exc_info=True)
        self.unloadMusic()
