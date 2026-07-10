const express = require("express");
const app = express();

app.use(express.json());

const products = [
  { id: 1, name: "Espresso", price: 50 }
];

app.get("/", (req, res) => {
  res.send("API is working ☕");
});

app.get("/products", (req, res) => {
  res.json(products);
});

app.listen(5000, () => {
  console.log("Running on port 5000");
});

app.post("/products", (req, res) => {
    const newProduct = {
      id: products.length + 1,
      name: req.body.name,
      price: req.body.price,
    };
  
    products.push(newProduct);
  
    res.status(201).json(newProduct);
  });