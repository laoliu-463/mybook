import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

class StringUtilTest {

    @Test
    @DisplayName("测试字符串反转 - 正常情况")
    void shouldReverseString() {
        // Arrange (准备)
        String input = "hello";
        
        // Act (执行)
        String result = new StringBuilder(input).reverse().toString();
        
        // Assert (断言)
        assertEquals("olleh", result, "字符串应该被反转");
    }

    @Test
    @DisplayName("测试空指针异常")
    void shouldThrowExceptionWhenNull() {
        String input = null;
        
        // 断言会抛出特定异常
        assertThrows(NullPointerException.class, () -> {
            new StringBuilder(input).reverse();
        });
    }
}