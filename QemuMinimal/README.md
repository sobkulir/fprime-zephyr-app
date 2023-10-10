# QemuMinimal

This is a minimal example that can be fully emulated. The target device is TI LM3S6965 which only has 64KiB RAM so I overrode the FpConfig with smaller buffers/array size etc to make it compile and run the basic example, but take that config with a grain of salt please.

## Building and running

Building is business as usual, running is a bit more involved.

### Building
```shell
$ fprime-util generate -DBOARD=qemu_cortex_m3 -DCMAKE_GENERATOR=Ninja
$ fprime-util build -j16
```

### Running
We need to run two processes from the container -- the Qemu emulator with the compiled code and a ground station server (GDS). The two will be connected together via a serial exposed to host as a pseudoterminal `/dev/pts/X`. Therefore, both the Qemu emulator and GDS need to be running in the same Docker container. To do this, `tmux` is installed in the Docker image and used below, but one can also for example start one of the processes in the background. 

Once built, open the `tmux` (terminal multiplexer, allows opening multiple terminals and managing them) and create another instance of a terminal:
```shell
$ tmux
$ # Ctrl+B % (creates new pane)
$ # Ctrl+B ; (switches focus between panes)
```

In one terminal, run the Qemu:
```shell
/opt/toolchains/zephyr-sdk-0.16.0/sysroots/x86_64-pokysdk-linux/usr/bin/qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb -nographic -vga none -net none -pidfile qemu.pid -chardev stdio,id=con,mux=on -serial chardev:con -mon chardev=con,mode=readline -icount shift=6,align=off,sleep=off -rtc clock=vm -kernel /zephyr-workspace/fprime-zephyr-app/QemuMinimal/build-fprime-automatic-zephyr/zephyr/zephyr.elf -serial pty
```
To exit Qemu, press `Ctrl+A X`. Normally, it would be enought to do `west build -t run`, but we need to pass the additional serial port for communication with the "ground" (the `-serial pty` at the end).

Notice which pseudoterminal on the host is exposed, it will be something like `char device redirected to /dev/pts/1 (label serial1)` in the output.

Now to run the GDS, switch the terminal to a new one (`Ctrl+B ;`) and run the following (make sure to change `/dev/pts/X` to the one Qemu opened in the last step):
```shell
sudo fprime-gds --uart-device /dev/pts/X --uart-baud 115200 --dictionary build-artifacts/zephyr/QemuMinimal/dict/QemuMinimalTopologyAppDictionary.xml -n --comm-adapter uart
```

Now, open `localhost:5000` in your browser and you should be able to send no-op commands (yay), see that the connection is alive in the upper right corner of the GDS..
