import os, sys, inspect, thread, time
import rtmidi_python as rtmidi
import libleap as Leap

class SampleListener(Leap.Listener):

    midi_out = None

    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.midi_out.open_virtual_port("Leap")
        super(SampleListener, self).__init__()

    def on_frame(self, controller):
        frame = controller.frame()
        hand = frame.hands.rightmost
        hand_cent = hand.palm_position
        mody = round((((hand_cent[1] - 45) / 400) * 127), 0)
        modx = round((((hand_cent[0] + 150) / 300) * 127), 0)
        modz = round((((hand_cent[2] + 150) / 300) * 127), 0)
        if mody > 127:
            mody = 127
        if mody < 0:
            mody = 0
        if modx > 127:
            modx = 127
        if modx < 0:
            modx = 0
        if modz > 127:
            modz = 127
        if modz < 0:
            modz = 0
        if hand.time_visible != 0:
            self.midi_out.send_message([0xB0, 3, mody])
            self.midi_out.send_message([0xB0, 9, modx])
            self.midi_out.send_message([0xB0, 14, modz])
            print mody, modx, modz


def main():
    midi_out = rtmidi.MidiOut()
    midi_out.open_virtual_port("Leap")
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
if __name__ == "__main__":
    main()