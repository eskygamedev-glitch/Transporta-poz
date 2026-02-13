#include <cpr/cpr.h>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    cpr::Header headers{
        {"Origin-Custom", "saraksti.lv"},
        {"User-Agent", "python-requests/2.31.0"},
        {"Accept", "*/*"},
        {"Connection", "keep-alive"}
    };

    while (true) {
        auto r = cpr::Get(
            cpr::Url{"https://saraksti.lv/gpsdata.ashx?gps"},
            headers
        );

        std::cout << "HTTP status: " << r.status_code << "\n";
        std::cout << r.text << "\n";

        std::cout << "Waiting 10 seconds...\n";
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }
}
