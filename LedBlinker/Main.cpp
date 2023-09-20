// ======================================================================
// \title  Main.cpp
// \brief main program for the F' application. Currently only prints to serial.
//
// ======================================================================
// Used to access topology functions
#include <LedBlinker/Top/LedBlinkerTopology.hpp>
#include <LedBlinker/Top/LedBlinkerTopologyAc.hpp>
#include <zephyr/kernel.h>

#include <zephyr/device.h>
#include <zephyr/fs/fs.h>
#include <zephyr/fs/littlefs.h>
#include <zephyr/logging/log.h>
#include <zephyr/storage/flash_map.h>

#include <zephyr/sys_clock.h>

#include <zephyr/drivers/gpio.h>

#define SPI_NHOLD_NODE DT_ALIAS(spi_nhold)
#define SPI_NWP_NODE DT_ALIAS(spi_nwp)


static const struct gpio_dt_spec spi_nhold_pin = GPIO_DT_SPEC_GET(SPI_NHOLD_NODE, gpios);
static const struct gpio_dt_spec spi_nwp_pin = GPIO_DT_SPEC_GET(SPI_NWP_NODE, gpios);

#define PARTITION_NODE DT_NODELABEL(lfs1)
FS_FSTAB_DECLARE_ENTRY(PARTITION_NODE);

LOG_MODULE_REGISTER(main);

int main()
{
    int ret;
    struct fs_mount_t *mp = &FS_FSTAB_ENTRY(PARTITION_NODE);

/*
    if (!gpio_is_ready_dt(&spi_nhold_pin)) {
        return;
    }*/

    ret = gpio_pin_configure_dt(&spi_nhold_pin, GPIO_OUTPUT_HIGH);
    if (ret < 0) {
        return 1;
    }
/*
    if (!gpio_is_ready_dt(&spi_nwp_pin)) {
        return;
    }*/

    ret = gpio_pin_configure_dt(&spi_nwp_pin, GPIO_OUTPUT_HIGH);
    if (ret < 0) {
        return 1;
    }

    if (IS_ENABLED(CONFIG_APP_WIPE_STORAGE)) {
        ret = fs_mkfs(FS_LITTLEFS, (uintptr_t)FIXED_PARTITION_ID(storage_partition), mp->fs_data, 0);
        if (ret < 0) {
            return 1;
        }
    }
    
    ret = fs_mount(mp);
    if (ret < 0) {
        LOG_PRINTK("FAIL: mount id %" PRIuPTR " at %s: %d\n",
               (uintptr_t)mp->storage_dev, mp->mnt_point, ret);
        return 1;
    }

    LedBlinker::TopologyState inputs;
    printk("Setting up topology\n");
    LedBlinker::setupTopology(inputs);
    printk("Topology running, entering simulatedCycle.\n");
    zephyrRateDriver.cycle(/*intervalUs=*/1 * USEC_PER_MSEC);

    // Should be never executed.
    while (1) ; 
    return 0;
}
