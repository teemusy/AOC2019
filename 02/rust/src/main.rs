use std::fs;


fn main() {
    let filename: &str = "../2_input.txt";
    let contents: String = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    let input: Vec<String> = contents.split(",").map(|n| n.to_string()).collect();
    let mut computer: Intcode = Intcode::new(input);

    // change values
    computer.code[1] = "12".to_string();
    computer.code[2] = "2".to_string();

    while !computer.ready {
        computer.step();
    }

    println!("{:#?}", computer)

}


#[derive(Debug)]
struct Intcode {
    code: Vec<String>,
    index: usize,
    ready: bool,
    return_codes: Vec<i32>
}

// Methods
impl Intcode{
    fn step(&mut self) {
        self.process();
    }

    fn process(&mut self) {
        let n: i32 = self.code[self.index].parse().unwrap();
        match n {
            1 => self.add(),
            2 => self.multiply(),
            99 => self.quit(),
            _ => println!("ERROR!")
        }
    }

    fn add(&mut self) {
        let noun: usize = self.code[self.index + 1].parse().unwrap();
        let verb: usize = self.code[self.index + 2].parse().unwrap();
        let position: usize = self.code[self.index + 3].parse().unwrap();
        let noun: i32 = self.code[noun].parse().unwrap();
        let verb: i32 = self.code[verb].parse().unwrap();
        self.code[position] = (noun + verb).to_string();
        self.index += 4;
    }

    fn multiply(&mut self) {
        let noun: usize = self.code[self.index + 1].parse().unwrap();
        let verb: usize = self.code[self.index + 2].parse().unwrap();
        let position: usize = self.code[self.index + 3].parse().unwrap();
        let noun: i32 = self.code[noun].parse().unwrap();
        let verb: i32 = self.code[verb].parse().unwrap();
        self.code[position] = (noun * verb).to_string();
        self.index += 4;
    }

    fn quit(&mut self) {
        self.ready = true;
    }

}

// Related functions
impl Intcode{
    fn new(code: Vec<String>) -> Intcode{
        Intcode{
            code,
            index: 0,
            ready: false,
            return_codes: Vec::new()
        }
    }
}