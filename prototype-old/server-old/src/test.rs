
struct Foo {
    a: i32
}

impl Foo {
    fn foo(&mut self) {
        println!("hello world");
    }
}


fn main() {
    let mut ffoo = Foo { a: 32 };

    ffoo.foo();
}
