const items = require('./items_data.json');
var v = require('vec3');
const mineflayer = require('mineflayer');

const { Movements, pathfinder } = require('mineflayer-pathfinder');
const { goals } = require('mineflayer-pathfinder');

const bot = mineflayer.createBot({
  host: 'bandryk.aternos.me',
  username: 'shurik',
  port: 56361,
  version: '1.20',
});
bot.loadPlugin(pathfinder);

async function drop_id(bot, _id, username) {
  const count = bot.inventory.count(_id);
  if (count > 0) {
    targetPlayer = bot.players[username];
    playerPosition = targetPlayer.entity.position;
    point = v(playerPosition.x, playerPosition.y, playerPosition.z);
    await bot.lookAt(point)
    await bot.toss(_id, null, count);
    bot.chat('На!');
  } else {
    bot.chat('Нема.');
  }
}

async function inventory(bot) {
  try {
    const inventoryItems = bot.inventory.items();
    if (inventoryItems.length === 0) {
      bot.chat('Мій інвентар порожній.');
    } else if (inventoryItems.length <= 5) {
      bot.chat(inventoryItems.map(item => `${item.name} x${item.count}`).join(', '));
    } else {
      for (const item of inventoryItems) {
        await bot.chat(`${item.name} x${item.count}`);
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
  } catch (err) {
    bot.chat('Помилка при отриманні інвентаря: ' + err.message);
  }
}

async function dropAll(bot, username) {
  const inventoryItems = bot.inventory.items();
  if (inventoryItems.length === 0) {
    bot.chat('Мій інвентар порожній.');
    return;
  }
  targetPlayer = bot.players[username];
  playerPosition = targetPlayer.entity.position;
  point = v(playerPosition.x, playerPosition.y, playerPosition.z);
  await bot.lookAt(point)
  for (const item of inventoryItems) {
    await bot.toss(item.type, null, item.count);
    await new Promise(resolve => setTimeout(resolve, 100)); // Delay of 100ms
  }
  bot.chat('Віддав усе.');
}


async function mineWood(bot, amount) {
  try {
    const mcData = require('minecraft-data')(bot.version);

    // Find nearest wood blocks
    const woodBlocks = bot.findBlocks({
      matching: block => block.name.includes('log'),
      maxDistance: 124,
      count: amount,
    });

    if (woodBlocks.length === 0) {
      bot.chat("Немає дерева поблизу.");
      return;
    }

    // Sort blocks by distance to ensure the bot mines from nearest to farthest
    woodBlocks.sort((a, b) => bot.entity.position.distanceTo(a) - bot.entity.position.distanceTo(b));

    // Set up pathfinding
    const movements = new Movements(bot, mcData);
    bot.pathfinder.setMovements(movements);

    for (const position of woodBlocks) {
      const block = bot.blockAt(position);

      if (block && bot.canDigBlock(block)) {
        // Path to the block before digging
        const goal = new goals.GoalBlock(block.position.x, block.position.y, block.position.z);
        await bot.pathfinder.goto(goal);

        await bot.dig(block);
      } else {
        bot.chat("Не можу дістати");
        return;
      }
    }

    bot.chat("Закінчив добувати дерево.");
  } catch (err) {
    bot.chat("Помилка при добуванні дерева: " + err.message);
  }
}


async function come(bot, username, cords) {
  targetPlayer = bot.players[username];
  if (targetPlayer) {
    //playerPosition = targetPlayer.entity.position;
    movements = new Movements(bot, require('minecraft-data')(bot.version));
    bot.pathfinder.setMovements(movements);
    goal = new goals.GoalBlock(cords[0], cords[1], cords[2]);

    //goal = new goals.GoalBlock(playerPosition.x, playerPosition.y, playerPosition.z);

    bot.chat(`Йду до ${username}.`);
    await bot.pathfinder.goto(goal, false);
    bot.chat(`Я на місці, ${username}!`);
  } else {
    bot.chat(`Не можу знайти гравця ${username}.`);
  }
}


bot.on('spawn', () => {
  bot.look(40, 0, true);
});

// bot.on('physicTick', async () => {
//   const mob = bot.nearestEntity(entity => entity.mobType && entity.mobType.includes('hostile'));
//   if (mob) {
//     const goal = new goals.GoalBlock(mob.position.x, mob.position.y, mob.position.z);
//     await bot.pathfinder.goto(goal);
//     await bot.attack(mob, false); // attack without swinging
//   }
// });

bot.on('path_update', (results) => {
  if (results.status === 'noPath') {
    console.log('Шлях не знайдено!');
  }
});


bot.on('chat', async (username, message) => {
  if (username === bot.username) return;

  const messageParts = message.split(/\s+/);
  const command = messageParts[0].toLowerCase();
  const item = messageParts.slice(1).join(' ').toLowerCase();

  if (command === 'кинь') {
    if (item in items) {
      drop_id(bot, items[item], username);
    } else {
      bot.chat(`Я не знаю, що таке "${item}".`);
    }
  } else if (message === 'інвентар') {
    inventory(bot)
  } else if (message === 'віддай все') {
    dropAll(bot, username);
  } else if (command === 'добудь') {
    mineWood(bot, item)
  } else if (command === 'прийди') {
    try {
      cords = item.split(" ")
      come(bot, username, cords)
    } catch { bot.chat("Щось пішло не так(") }
  }
}
)
