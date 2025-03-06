const express = require('express');
const path = require('path');
const app = express();
const port = 8097;

app.use(express.static('public'));

const products = [
    { id: 1, name: "Beginner's Wand", description: "A simple wand for new wizards.", price: 10, image: "https://static.wikia.nocookie.net/realminescape/images/2/28/Beginner%27s_wand.png" },
    { id: 2, name: "Enchanted Spellbook", description: "A book filled with basic spells.", price: 25, image: "https://static.wikia.nocookie.net/flag-wars/images/d/da/Ebook.png" },
    { id: 3, name: "Potion of Minor Healing", description: "Restores a small amount of health.", price: 5, image: "https://static.wikia.nocookie.net/skyrim_gamepedia/images/0/0a/PotionofMinorHealing.png" },
    { id: 4, name: "Flag Part 1", description: "ARKAV{H1dden_", price: 50, image: "images/phoenix_feather.jpg" },
    { id: 5, name: "Magic Cloak", description: "Provides basic protection against the elements.", price: 30, image: "https://static.wikia.nocookie.net/lovenikki/images/6/6b/Magic_Cloak.png" },
    { id: 6, name: "Ring of Luck", description: "Increases good fortune slightly.", price: 40, image: "https://runescape.wiki/images/Ring_of_Luck_detail.png?945ed" },
    { id: 7, name: "Wizard's Hat", description: "A stylish hat that enhances minor spells.", price: 20, image: "https://static.wikia.nocookie.net/harrypotter/images/6/62/Sorting_Hat.png" },
    { id: 8, name: "Mystic Orb", description: "A crystal orb that glows in the dark.", price: 35, image: "https://runescape.wiki/images/Mystic_orb_detail.png?b0464" },
    { id: 9, name: "Scroll of Fireball", description: "Allows the user to cast a fireball once.", price: 15, image: "https://static.wikia.nocookie.net/day-r/images/3/30/Scroll_fireball.png" },
    { id: 10, name: "Flying Broomstick", description: "A broom that hovers slightly when used.", price: 100, image: "https://static.wikia.nocookie.net/harrypotter/images/8/8d/Broomsticks.jpg" },
    { id: 11, name: "Elixir of Wisdom", description: "Increases intelligence temporarily.", price: 60, image: "https://ih1.redbubble.net/image.1253573873.1432/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.u1.webp" },
    { id: 12, name: "Crystal Ball", description: "Glimpses into possible futures.", price: 80, image: "https://static.wikia.nocookie.net/hitman/images/6/67/Crystal_Ball_HITMAN2021.jpeg" },
    { id: 13, name: "Shield of Reflection", description: "Can reflect minor spells.", price: 90, image: "https://static.wikia.nocookie.net/dynastio/images/f/f4/Shield_Of_Reflection.png" },
    { id: 14, name: "Spell of Teleportation", description: "Instantly transports you to a known location.", price: 120, image: "http://wiki.alexissmolensk.com/images/5/54/Teleport.jpg" },
    { id: 15, name: "Summoning Scroll", description: "Summons a friendly spirit for assistance.", price: 75, image: "https://static.wikia.nocookie.net/naruto/images/6/6a/Toad_Contract_Scroll.png" },
    { id: 43, name: "Flag Part 2", description: "product_found_", price: 50, image: "images/phoenix_feather.jpg" },
    { id: 99, name: "Ancient Dragon's Heart", description: "A forbidden relic of immense power.", price: 0, image: "https://eldenring.wiki.fextralife.com/file/Elden-Ring/dragon_heart_elden_ring_wiki_guide_200px.png" },
    { id: 100, name: "Flag Part 3", description: "0p3ns_Secr3t_P4th}.", price: 0, image: "" }
];

app.get('/products', (req, res) => {
    // Exclude flag-related products from the response
    const visibleProducts = products.filter(p => ![4, 43, 100].includes(p.id));
    res.json(visibleProducts);
});

app.get('/product', (req, res) => {
    let productId = parseInt(req.query.productId);
    const product = products.find(p => p.id === productId);

    if (product) {
        res.json({ success: true, product });
    } else {
        res.status(404).json({ success: false, message: "Product not found" });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
