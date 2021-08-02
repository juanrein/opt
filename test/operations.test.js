const ops = require("./operations");

test("crossover", () => {
    expect(ops.integer_crossover(0b1111, 0b0000)).toEqual([0b1100, 0b0011]);    
});