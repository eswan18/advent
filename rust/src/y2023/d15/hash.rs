pub fn hash(s: &str) -> u32 {
    let mut current = 0;
    for c in s.chars() {
        let ascii = c as u32;
        current += ascii;
        current *= 17;
        current %= 256;
    }
    current
}