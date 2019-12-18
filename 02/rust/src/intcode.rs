use std::process;

#[derive(Debug)]
pub(crate) struct Intcode {
    pub(crate) code: Vec<i32>,
    index: usize,
    pub(crate) ready: bool,
    return_codes: Vec<i32>,
    pub(crate) instruction: i32,
    output: i32,
    new_output: bool
}

// Methods
impl Intcode{
    pub(crate) fn step(&mut self) -> (i32, bool){

        self.process();
        if self.new_output {
            self.new_output = false;
            return (self.output, true)
        }
        return (self.output, false)



    }

    fn process(&mut self) {
        let mut n: i32 = self.code[self.index];
        // parse parameters
        let tenthousands: i32 = n / 10000;
        let thousands: i32 = n / 1000 % 100;
        let hundreds: i32 = n / 100 % 10;
        let param: (i32, i32, i32) = (hundreds, thousands, tenthousands);
        n = n % 10000 % 1000 % 100;
        match n {
            1 => self.add(param),
            2 => self.multiply(param),
            3 => self.input(param),
            4 => self.output(param),
            5 => self.jumpiftrue(param),
            6 => self.jumpiffalse(param),
            7 => self.lessthan(param),
            8 => self.equals(param),
            99 => self.quit(),
            _ => {println!("ERROR!\nIntcode: {:?} \nParameters: {:?}", self, param); process::exit(0x0100);}
        }
    }

    fn add(&mut self, param: (i32, i32, i32)) {
        let mut noun: i32 = self.code[self.index + 1];
        let mut verb: i32 = self.code[self.index + 2];
        let mut position: usize = self.code[self.index + 3] as usize;
        if param.0 == 0 {
            noun = self.code[noun as usize];
        }
        if param.1  == 0 {
            verb = self.code[verb as usize];
        }
        if param.2 == 1 {
            position = self.code[position] as usize;
        }

        self.code[position] = noun + verb;
        self.index += 4;
    }

    fn multiply(&mut self, param: (i32, i32, i32)) {
        let mut noun: i32 = self.code[self.index + 1];
        let mut verb: i32 = self.code[self.index + 2];
        let mut position: usize = self.code[self.index + 3] as usize;
        if param.0 == 0 {
            noun = self.code[noun as usize];
        }
        if param.1  == 0 {
            verb = self.code[verb as usize];
        }
        if param.2 == 1 {
            position = self.code[position] as usize;
        }

        self.code[position] = noun * verb;
        self.index += 4;
    }

    fn input(&mut self, param: (i32, i32, i32)) {
        let mut position: usize = self.code[self.index + 1] as usize;
        if param.0 == 1 {
            position = self.code[position] as usize;
        }

        self.code[position] = self.instruction;
        self.index += 2;
    }

    fn output(&mut self, param: (i32, i32, i32)){
        let mut position: usize = self.code[self.index + 1] as usize;
        if param.0 == 1 {
            position = self.code[position] as usize;
        }

        self.output = self.code[position];
        self.new_output = true;
        self.return_codes.push(self.output);
        self.index += 2;
    }

    fn jumpiftrue(&mut self, param: (i32, i32, i32)) {
        let mut noun: i32 = self.code[self.index + 1];
        let mut position: usize = self.code[self.index + 2] as usize;
        if param.0 == 0 {
            noun = self.code[noun as usize];
        }
        if param.1 == 0 {
            position = self.code[position] as usize;
        }
        if self.code[noun as usize] != 0 {
            self.index = self.code[position] as usize;
        }
        else {
            self.index += 3;
        }
    }

    fn jumpiffalse(&mut self, param: (i32, i32, i32)) {
        let mut noun: i32 = self.code[self.index + 1];
        let mut position: usize = self.code[self.index + 2] as usize;
        if param.0 == 0 {
            noun = self.code[noun as usize];
        }
        if param.1 == 0 {
            position = self.code[position] as usize;
        }
        if self.code[noun as usize] == 0 {
            self.index = self.code[position] as usize;
        }
        else {
            self.index += 3;
        }
    }

    fn lessthan(&mut self, param: (i32, i32, i32)) {
        let mut noun: i32 = self.code[self.index + 1];
        let mut verb: i32 = self.code[self.index + 2];
        let mut position: usize = self.code[self.index + 3] as usize;
        if param.0 == 0 {
            noun = self.code[noun as usize];
        }
        if param.1  == 0 {
            verb = self.code[verb as usize];
        }
        if param.2 == 1 {
            position = self.code[position] as usize;
        }
        if noun < verb {
            self.code[position] = 1;
        }
        else {
            self.code[position] = 0;
        }
        self.index += 4;
    }

    fn equals(&mut self, param: (i32, i32, i32)) {
        let mut noun: i32 = self.code[self.index + 1];
        let mut verb: i32 = self.code[self.index + 2];
        let mut position: usize = self.code[self.index + 3] as usize;
        if param.0 == 0 {
            noun = self.code[noun as usize];
        }
        if param.1  == 0 {
            verb = self.code[verb as usize];
        }
        if param.2 == 1 {
            position = self.code[position] as usize;
        }
        if noun == verb {
            self.code[position] = 1;
        }
        else {
            self.code[position] = 0;
        }
        self.index += 4;
    }

    pub(crate) fn set_input(&mut self, instruction: i32) {
        self.instruction = instruction;
    }

    fn quit(&mut self) {
        self.ready = true;
    }
}

// Related functions
impl Intcode{
    pub(crate) fn new(code: Vec<i32>) -> Intcode{
        Intcode{
            code,
            index: 0,
            ready: false,
            return_codes: Vec::new(),
            instruction: 0,
            output: 0,
            new_output: false
        }
    }
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn position1() {
        let input = "3,9,8,9,10,9,4,9,99,-1,8".to_string();
        let mut output: (i32, bool) = (0, false);
        let input: Vec<i32> = input.split(",").map(|n| n.parse().unwrap()).collect();
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(8);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 1);
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(5);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 0);
    }

    #[test]
    fn position2() {
        let input = "3,9,7,9,10,9,4,9,99,-1,8".to_string();
        let mut output: (i32, bool) = (0, false);
        let input: Vec<i32> = input.split(",").map(|n| n.parse().unwrap()).collect();
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(5);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 1);
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(8);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 0);
    }

    #[test]
    fn immediate1() {
        let input = "3,3,1108,-1,8,3,4,3,99".to_string();
        let mut output: (i32, bool) = (0, false);
        let input: Vec<i32> = input.split(",").map(|n| n.parse().unwrap()).collect();
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(8);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 1);
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(45);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 0);
    }

    #[test]
    fn immediate2() {
        let input = "3,3,1107,-1,8,3,4,3,99".to_string();
        let mut output: (i32, bool) = (0, false);
        let input: Vec<i32> = input.split(",").map(|n| n.parse().unwrap()).collect();
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(-45);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 1);
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(45);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 0);
    }

    #[test]
    fn position3() {
        let input = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".to_string();
        let mut output: (i32, bool) = (0, false);
        let input: Vec<i32> = input.split(",").map(|n| n.parse().unwrap()).collect();
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(0);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 0);
        let mut computer: Intcode = Intcode::new(input.clone());
        computer.set_input(45);
        while !computer.ready{
            output = computer.step();
        }
        assert_eq!(output.0, 1);
    }
}