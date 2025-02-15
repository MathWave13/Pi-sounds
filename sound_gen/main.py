
import time
import numpy as np
import pyaudio
import keyboard
from decimal import Decimal, getcontext

frequencies = {
    0: 261, 
    1: 293, 
    2: 329, 
    3: 349, 
    4: 392, 
    5: 440, 
    6: 493, 
    7: 523, 
    8: 587, 
    9: 659  
}

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

def generate_fade_wave(frequency, duration=0.7, sample_rate=44100, wave_type='sawtooth'):
    """Generate a fading synth wave with a modern ambient feel."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if wave_type == 'sawtooth':
        wave = 0.7 * (1 - 2 * (t * frequency - np.floor(t * frequency + 0.5)))
    elif wave_type == 'square':
        wave = np.sign(np.sin(2 * np.pi * frequency * t))
    else:
        wave = np.sin(2 * np.pi * frequency * t)
    
    fade_out = np.exp(-3 * t)
    modulator = np.sin(2 * np.pi * 1.5 * t) * 0.2
    return ((wave + modulator) * fade_out).astype(np.float32)

def play_blended_tone(frequency, prev_wave=None):
    """Play a tone while blending with the previous tone for a continuous flow."""
    new_wave = generate_fade_wave(frequency, duration=0.4, wave_type='sine')
    if prev_wave is not None:
        blended_wave = (prev_wave * 0.5 + new_wave * 0.5)
    else:
        blended_wave = new_wave
    
    stream.write(blended_wave.tobytes())
    return new_wave

def pi_digits():
    getcontext().prec = 2000
    pi_str = str(Decimal(3.141592653589793))
    
    while True:
        for digit in pi_str[2:]:
            yield int(digit)

def main():
    pi_gen = pi_digits()
    paused = False
    prev_wave = None

    print("🎵 Playing Pi Digits Sound... Press [SPACE] to Pause/Resume, [Q] to Quit.")

    while True:
        if keyboard.is_pressed('space'):
            paused = not paused
            print("⏸ Paused" if paused else "▶ Resumed")
            time.sleep(0.3)

        if keyboard.is_pressed('q'):
            print("👋 Quitting...")
            break

        if not paused:
            digit = next(pi_gen)
            print(f"🎶 Playing digit: {digit}", flush=True)
            prev_wave = play_blended_tone(frequencies[digit], prev_wave)
            time.sleep(0.1)

    close_audio()

def close_audio():
    """Stop and close the audio stream."""
    stream.stop_stream()
    stream.close()
    p.terminate() 

if __name__ == "__main__":
    main()
  