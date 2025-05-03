#include "qemu/osdep.h"
#include "qemu/units.h"
#include "hw/pci/pci.h"
#include "hw/hw.h"
#include "hw/pci/msi.h"
#include "qom/object.h"
#include "qemu/module.h"
#include "qapi/visitor.h"
#include "sysemu/dma.h"

#define TARGETS_COUNT 1024
#define MAX_SHOTS_PER_SESSION 6

typedef struct LaserState {
    PCIDevice pdev;
    MemoryRegion mmio;
    AddressSpace *as;

    uint64_t targets[TARGETS_COUNT];

    struct control {
        dma_addr_t shots[MAX_SHOTS_PER_SESSION];
        dma_addr_t shot_count;
        dma_addr_t pattern;
    } ctrl;

    int hits;
} LaserState;

DECLARE_INSTANCE_CHECKER(LaserState, PEWPEWPEW, "pewpewpew")

#define MMIO_OFFSET_SHOT1 0x8
#define MMIO_OFFSET_SHOT2 0x10
#define MMIO_OFFSET_SHOT3 0x18
#define MMIO_OFFSET_SHOT4 0x20
#define MMIO_OFFSET_SHOT5 0x28
#define MMIO_OFFSET_SHOT6 0x30
#define MMIO_OFFSET_SHOT_COUNT 0x38

#define MMIO_OFFSET_PATTERN 0x40
#define MMIO_OFFSET_HITS 0x48
#define MMIO_TRIGGER_FIRE 0x50


static void fire_laser(LaserState* s) {
    for (int i = 0; i < s->ctrl.shot_count; ++i) {
        int pos = s->ctrl.shots[i];
        uint64_t target = s->targets[pos];
        uint64_t pattern = s->ctrl.pattern;
        int bit = 0;

        while (pattern) {
            if (target & pattern & 1) {
                s->hits++;
            }

            if (pattern & 1) {
                s->targets[pos] ^= (1UL << bit);
            }

            target >>= 1;
            pattern >>= 1;
            bit++;
        }
    }
}

static uint64_t mmio_read(void *opaque, hwaddr addr, unsigned size)
{
    LaserState *s = opaque;
    uint64_t val = 0;

    switch (addr) {
        case MMIO_OFFSET_SHOT1:
        case MMIO_OFFSET_SHOT2:
        case MMIO_OFFSET_SHOT3:
        case MMIO_OFFSET_SHOT4:
        case MMIO_OFFSET_SHOT5:
        case MMIO_OFFSET_SHOT6:
            int idx = (addr - MMIO_OFFSET_SHOT1) / 8;
            val = s->ctrl.shots[idx];
            break;
        case MMIO_OFFSET_SHOT_COUNT:
            val = s->ctrl.shot_count;
            break;
        case MMIO_OFFSET_PATTERN:
            val = s->ctrl.pattern;
            break;
        case MMIO_OFFSET_HITS:
            val = s->hits;
            break;
    }

    return val;
}

static void mmio_write(void *opaque, hwaddr addr, uint64_t val,
                unsigned size)
{
    LaserState *s = opaque;

    switch (addr) {
        case MMIO_OFFSET_SHOT1:
        case MMIO_OFFSET_SHOT2:
        case MMIO_OFFSET_SHOT3:
        case MMIO_OFFSET_SHOT4:
        case MMIO_OFFSET_SHOT5:
        case MMIO_OFFSET_SHOT6:
            int idx = (addr - MMIO_OFFSET_SHOT1) / 8;
            if (val <= TARGETS_COUNT) {
                s->ctrl.shots[idx] = val;
            }
            break;
        case MMIO_OFFSET_SHOT_COUNT:
            s->ctrl.shot_count = val;
            break;
        case MMIO_OFFSET_PATTERN:
            s->ctrl.pattern = val;
            break;
        case MMIO_TRIGGER_FIRE:
            fire_laser(s);
            break;
    }
}

static const MemoryRegionOps mmio_ops = {
    .read = mmio_read,
    .write = mmio_write,
    .endianness = DEVICE_NATIVE_ENDIAN,
    .valid = {
        .min_access_size = 4,
        .max_access_size = 8,
    },
    .impl = {
        .min_access_size = 4,
        .max_access_size = 8,
    },
};

static void realize(PCIDevice *pdev, Error **errp)
{
    LaserState *s = PEWPEWPEW(pdev);

    if (msi_init(pdev, 0, 1, true, false, errp)) {
        return;
    }

    s->as = &address_space_memory;
    memory_region_init_io(&s->mmio, OBJECT(s), &mmio_ops, s,
                    "pewpewpew-mmio", 1 * MiB);
    pci_register_bar(pdev, 0, PCI_BASE_ADDRESS_SPACE_MEMORY, &s->mmio);
}

static void uninit(PCIDevice *pdev)
{
    msi_uninit(pdev);
}

static void instance_init(Object *obj)
{
}

static void class_init(ObjectClass *class, void *data)
{
    DeviceClass *dc = DEVICE_CLASS(class);
    PCIDeviceClass *k = PCI_DEVICE_CLASS(class);

    k->realize = realize;
    k->exit = uninit;
    k->vendor_id = 0xbabe;
    k->device_id = 0xbeef;
    k->revision = 0x45;
    k->class_id = PCI_CLASS_OTHERS;
    set_bit(DEVICE_CATEGORY_MISC, dc->categories);
}

static void pci_register_types(void)
{
    static InterfaceInfo interfaces[] = {
        { INTERFACE_CONVENTIONAL_PCI_DEVICE },
        { },
    };

    static const TypeInfo info = {
        .name          = "pewpewpew",
        .parent        = TYPE_PCI_DEVICE,
        .instance_size = sizeof(LaserState),
        .instance_init = instance_init,
        .class_init    = class_init,
        .interfaces = interfaces,
    };

    type_register_static(&info);
}
type_init(pci_register_types)