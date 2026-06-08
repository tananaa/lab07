#include <gtest/gtest.h>
#include "print.hpp"
#include <sstream>

TEST(PrintTest, PrintToCout) {
    testing::internal::CaptureStdout();
    print("hello");
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output, "hello\n");
}

TEST(PrintTest, PrintToOstream) {
    std::stringstream ss;
    print("hello", ss);
    EXPECT_EQ(ss.str(), "hello\n");
}
