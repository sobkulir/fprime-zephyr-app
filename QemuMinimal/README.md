fprime-util generate -DBOARD=qemu_cortex_m3 -DCMAKE_GENERATOR=Ninja

fprime-util build -j16

/opt/toolchains/zephyr-sdk-0.16.0/sysroots/x86_64-pokysdk-linux/usr/bin/qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb -nographic -vga none -net none -pidfile qemu.pid -chardev stdio,id=con,mux=on -serial chardev:con -mon chardev=con,mode=readline -icount shift=6,align=off,sleep=off -rtc clock=vm -kernel /zephyr-workspace/fprime-zephyr-app/QemuMinimal/build-fprime-automatic-zephyr/zephyr/zephyr.elf -serial pty


sudo fprime-gds --uart-device /dev/pts/3 --uart-baud 115200 --dictionary build-artifacts/zephyr/QemuMinimal/dict/QemuMinimalTopologyAppDictionary.xml -n --comm-adapter uart