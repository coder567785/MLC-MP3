import gi
import os
import sys
import vlc

# Initialize GTK
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

class MLCMP3Player(Gtk.Window):
    def __init__(self):
        super().__init__(title="MLC MP3 Player")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        self.init_ui()
        self.player = vlc.MediaPlayer()
        self.playing = False

    def init_ui(self):
        # Main Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Playlist Area
        playlist_frame = Gtk.Frame(label="📋 Playlists")
        playlist_scrolled = Gtk.ScrolledWindow()
        playlist_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.playlist_listbox = Gtk.ListBox()
        playlist_scrolled.add(self.playlist_listbox)
        playlist_frame.add(playlist_scrolled)
        vbox.pack_start(playlist_frame, True, True, 0)

        # Controls Area
        controls_box = Gtk.Box(spacing=10)
        open_button = Gtk.Button(label="📂 Open")
        open_button.connect("clicked", self.on_open_clicked)
        shuffle_button = Gtk.Button(label="🔀 Shuffle")
        repeat_button = Gtk.Button(label="🔁 Repeat")
        play_button = Gtk.Button(label="▶️ Play")
        play_button.connect("clicked", self.on_play_clicked)
        stop_button = Gtk.Button(label="⏹️ Stop")
        stop_button.connect("clicked", self.on_stop_clicked)
        about_button = Gtk.Button(label="ℹ️ About")
        about_button.connect("clicked", self.on_about_clicked)

        controls_box.pack_start(open_button, True, True, 0)
        controls_box.pack_start(shuffle_button, True, True, 0)
        controls_box.pack_start(repeat_button, True, True, 0)
        controls_box.pack_start(play_button, True, True, 0)
        controls_box.pack_start(stop_button, True, True, 0)
        controls_box.pack_start(about_button, True, True, 0)
        vbox.pack_start(controls_box, False, False, 0)

        # Equalizer Area
        equalizer_frame = Gtk.Frame(label="🎚️ Equalizer")
        equalizer_box = Gtk.Box(spacing=10)
        self.scales = []
        for i in range(5):
            scale = Gtk.Scale(orientation=Gtk.Orientation.VERTICAL)
            scale.set_range(0, 100)
            scale.set_value(50)
            scale.connect("value-changed", self.on_equalizer_changed)
            self.scales.append(scale)
            equalizer_box.pack_start(scale, True, True, 0)
        equalizer_frame.add(equalizer_box)
        vbox.pack_start(equalizer_frame, False, False, 0)

        # Pitch Control
        pitch_frame = Gtk.Frame(label="🎵 Pitch")
        pitch_box = Gtk.Box(spacing=10)
        self.pitch_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.pitch_scale.set_range(0.5, 2.0)
        self.pitch_scale.set_value(1.0)
        self.pitch_scale.set_increments(0.1, 0.1)
        self.pitch_scale.connect("value-changed", self.on_pitch_changed)
        pitch_box.pack_start(self.pitch_scale, True, True, 0)
        pitch_frame.add(pitch_box)
        vbox.pack_start(pitch_frame, False, False, 0)

        # Status Bar
        self.status_bar = Gtk.Statusbar()
        self.status_context_id = self.status_bar.get_context_id("status")
        self.status_bar.push(self.status_context_id, "Ready")
        vbox.pack_start(self.status_bar, False, False, 0)

        # Show all widgets
        self.show_all()

    def on_open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose an MP3 file", parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_mp3 = Gtk.FileFilter()
        filter_mp3.set_name("MP3 files")
        filter_mp3.add_mime_type("audio/mpeg")
        dialog.add_filter(filter_mp3)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.media_path = dialog.get_filename()
            self.playlist_listbox.add(Gtk.Label(label=os.path.basename(self.media_path)))
            self.playlist_listbox.show_all()
            self.status_bar.push(self.status_context_id, f"Loaded: {os.path.basename(self.media_path)}")
        dialog.destroy()

    def on_play_clicked(self, widget):
        if hasattr(self, 'media_path') and not self.playing:
            self.player.set_media(vlc.Media(self.media_path))
            self.player.play()
            self.playing = True
            self.status_bar.push(self.status_context_id, "Playing...")

    def on_stop_clicked(self, widget):
        if self.playing:
            self.player.stop()
            self.playing = False
            self.status_bar.push(self.status_context_id, "Stopped")

    def on_equalizer_changed(self, widget):
        # Placeholder: Implement equalizer logic as needed
        pass

    def on_pitch_changed(self, widget):
        pitch_value = self.pitch_scale.get_value()
        if self.player.is_playing():
            self.player.set_rate(pitch_value)
        self.status_bar.push(self.status_context_id, f"Pitch: {pitch_value:.2f}")

    def on_about_clicked(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_program_name("MLC MP3 Player")
        about_dialog.set_version("1.0")
        about_dialog.set_comments("A sleek, modern, and feature-packed MP3 player.")
        about_dialog.set_website("https://example.com")
        about_dialog.run()
        about_dialog.destroy()

if __name__ == "__main__":
    app = MLCMP3Player()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()
