import re

class HardwareOSErrorDetector:

    def __init__(self):
        self.patterns = {

            # CPU Errors
            "CPU_ERRORS": [
                r"cpu overheating",
                r"thermal throttling",
                r"machine check exception",
                r"cpu fan failure",
                r"cpu core failure",
                r"cpu clock throttled",
                r"soft lockup",
                r"watchdog timeout"
            ],

            # Memory Errors
            "MEMORY_ERRORS": [
                r"out of memory",
                r"memory leak",
                r"segmentation fault",
                r"sigsegv",
                r"memory read error",
                r"ecc memory error",
                r"stack overflow",
                r"heap corruption"
            ],

            # Disk / Storage Errors
            "DISK_ERRORS": [
                r"disk read error",
                r"disk write error",
                r"bad sector",
                r"smart.*failed",
                r"i/o error",
                r"failed command",
                r"nvme.*timeout",
                r"file system corruption"
            ],

            # Network Hardware Errors
            "NETWORK_HARDWARE_ERRORS": [
                r"network card failure",
                r"nic error",
                r"link down",
                r"cable unplugged",
                r"crc error",
                r"packet loss",
                r"duplex mismatch"
            ],

            # Power & Cooling
            "POWER_COOLING_ERRORS": [
                r"power supply failure",
                r"voltage out of range",
                r"ups battery failure",
                r"temperature exceeded",
                r"fan failure",
                r"thermal zone",
                r"overheat"
            ],

            # GPU Errors
            "GPU_ERRORS": [
                r"gpu overheating",
                r"gpu driver crash",
                r"vram error",
                r"display driver stopped",
                r"cuda error",
                r"vulkan device lost"
            ],

            # Kernel / OS Errors
            "KERNEL_ERRORS": [
                r"kernel panic",
                r"blue screen",
                r"bsod",
                r"kernel oops",
                r"system crash",
                r"system hang",
                r"bugcheck"
            ],

            # Boot Errors
            "BOOT_ERRORS": [
                r"boot device not found",
                r"bootloader error",
                r"grub error",
                r"initramfs error",
                r"bcd error"
            ],

            # Driver Errors
            "DRIVER_ERRORS": [
                r"driver failed",
                r"driver crash",
                r"driver timeout",
                r"driver not found",
                r"driver conflict"
            ],

            # I/O Errors
            "IO_ERRORS": [
                r"i/o device error",
                r"device not ready",
                r"device timeout",
                r"device offline",
                r"request cancelled"
            ],

            # File System Errors
            "FILESYSTEM_ERRORS": [
                r"file system corrupted",
                r"fsck failed",
                r"inode corruption",
                r"superblock error",
                r"disk full"
            ],

            # Virtualization Errors
            "VIRTUALIZATION_ERRORS": [
                r"hypervisor error",
                r"vm failed",
                r"vm migration failed",
                r"virtual cpu error",
                r"nested virtualization"
            ],

            # Hardware Monitoring
            "HARDWARE_MONITOR_ERRORS": [
                r"sensor failure",
                r"bmc unreachable",
                r"ipmi error",
                r"temperature sensor",
                r"fan speed low"
            ]
        }

    def detect(self, log_line):
        log_line = log_line.lower()

        matches = []

        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, log_line):
                    matches.append(category)
                    break

        if matches:
            return {
                "categories": list(set(matches)),
                "severity": self.get_severity(matches)
            }

        return {"categories": ["UNKNOWN"], "severity": "LOW"}

    def get_severity(self, categories):
        severity_map = {
            "CPU_ERRORS": "CRITICAL",
            "KERNEL_ERRORS": "CRITICAL",
            "DISK_ERRORS": "HIGH",
            "MEMORY_ERRORS": "HIGH",
            "POWER_COOLING_ERRORS": "HIGH",
            "GPU_ERRORS": "MEDIUM",
            "DRIVER_ERRORS": "MEDIUM",
            "IO_ERRORS": "MEDIUM"
        }

        for cat in categories:
            if cat in severity_map:
                return severity_map[cat]

        return "LOW"