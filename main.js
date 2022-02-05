const mysql = require('mysql2');
const Discord = require('discord.js');
const { Permissions } = require('discord.js');
const client = new Discord.Client({ autoReconnct: true });
const yargs = require('yargs/yargs');

const config = require("./config.json");

const CARD = 'card';
const IDOL = 'idol';
const HELP = 'help';
const KICK = 'kick';
const RAPE = 'rape';
const PNCH = 'punch';

client.once('ready', () => {
    client.user.setActivity("ShinyColorsBot  #help");
    console.log('Ready!');
});

client.login(config.token);

let conn;

connectDB();

function connectDB() {
    conn = new mysql.createConnection(config.database);
    conn.connect((err) => {
        if (err) {
            console.log("!!! Cannot connect !!! Error:");
            throw err;
        }
        else {
            console.log("Connection established.");
        }
    });

    conn.on('error', (err) => {
        if (err.code == 'PROTOCOL_CONNECTION_LOST' || err.code == 'PROTOCOL_UNEXPECTED_PACKET') {
            conn = null;
            connectDB();
        } else {
            conn = null;
            throw err;
        }
    });
}

client.on('message', async (msg) => {
    if (!msg.content.match(/^\#/)) return;

    let command = msg.content.match(/^\#([^\s]*)/)[1];


    let args = yargs().parse(msg.content.replace(/^\#([^\s]*) /, '').split(" "));

    console.log(command, args);

    switch (command) {
        case CARD: {
            if ((!args?.n && !args?.t) || !args?.i) {
                msg.reply("至少需要兩項參數以進行搜尋");
                return;
            }

            let idol = args?.i ? args.i : ".*",
                card = args?.n ? args.n : ".*",
                type = args?.t ? args.t : ".*";

            conn.execute(
                'SELECT a.*, b.Color1 FROM `SCDB_CardList` as a, `SCDB_Idols` as b WHERE b.IdolName REGEXP ? AND b.IdolID = a.IdolID AND a.CardName REGEXP ? AND a.CardType REGEXP ? ORDER BY FIELD(CardType, "P_SSR", "P_SR", "P_R", "S_SSR", "S_SR", "S_R", "S_N")',
                [idol, card, type],
                (err, result) => {
                    if (!result?.length) {
                        msg.reply("未找到符合條件的搜尋結果");
                    }
                    else if (result?.length > 10) {
                        msg.reply("有超過10筆結果，請使用更精確的參數進行搜尋=ˇ=");
                    }
                    else if (result?.length != 1) {
                        const embed = new Discord.MessageEmbed()
                            .setColor(result[0].Color1)
                            .setTitle("搜尋條件有以下的結果，請根據此清單進行更精確的搜尋");

                        result.forEach((element) => {
                            embed.addField(element.CardName, element.CardType);
                        });

                        msg.reply(embed);
                    }
                    else if (result?.length == 1) {
                        const type = result[0].CardType.match(/P_/) ? "P" : "S";
                        const picUrl = type == "P" ? result[0].BigPic2 : result[0].BigPic1;
                        const embed = new Discord.MessageEmbed()
                            .setColor(result[0].Color1)
                            .setTitle(result[0].CardName)
                            .setURL(`https://shinycolors.moe/info/${type}CardInfo?UUID=${result[0].CardUUID}`)
                            .setImage('https://static.shinycolors.moe/pictures/bigPic/' + picUrl + ".jpg")
                            .setThumbnail('https://static.shinycolors.moe/pictures/smlPic/' + result[0].SmallPic + ".png")
                            .setTimestamp()
                            .setFooter("Project ShinyColorsDB");

                        msg.reply(embed);
                    }
                });

            break;
        }
        case IDOL: {
            if (!args?.n) {
                msg.reply("需要角色名稱");
                return;
            }

            conn.execute(
                'SELECT a.*, b.UnitName FROM `SCDB_Idols` AS a, `SCDB_Units` AS b WHERE `IdolName` REGEXP ? AND a.Unit = b.UnitID',
                [args.n],
                (err, result) => {

                    //console.log(result);
                    if (!result?.length) {
                        msg.reply("No Result!");
                    }
                    else if (result?.length > 1) {
                        const embed = new Discord.MessageEmbed()
                            .setColor(result[0].Color1)
                            .setTitle("搜尋條件有以下的結果，請根據此清單進行更精確的搜尋");

                        result.forEach((element) => {
                            embed.addField(element.IdolName, element.CV);
                        });
                        msg.reply(embed);
                    }
                    else {
                        const embed = new Discord.MessageEmbed()
                            .setColor(result[0].Color1)
                            .setTitle(result[0].IdolName)
                            .addField("ひらがな", result[0].Hiragana, true)
                            .addField("ユニット", result[0].UnitName, true)
                            .addField("\u200B", "\u200B", false)
                            .addField("年齢", result[0].Age, true)
                            .addField("誕生日", result[0].BirthDay, true)
                            .addField("星座", result[0].StarSign, true)
                            .addField("血型", result[0].BloodType, true)
                            .addField("\u200B", "\u200B", false)
                            .addField("身長", result[0].Height, true)
                            .addField("体重", result[0].Weight, true)
                            .addField("出身地", result[0].BirthPlace, true)
                            .addField("スリーサイズ", result[0].ThreeSize, true)
                            .addField("\u200B", "\u200B", false)
                            .addField("趣味", result[0].Interest)
                            .addField("特技", result[0].SpecialSkill)
                            .addField("CV", result[0].CV)
                            .setThumbnail(`https://static.shinycolors.moe/pictures/icon/${result[0].NickName}.jpg`)
                            .setImage(`https://static.shinycolors.moe/pictures/tachie/private/${result[0].NickName}.png`)
                            .setTimestamp()
                            .setFooter("Project ShinyColorsDB");

                        msg.reply(embed);
                    }


                });

            break;
        }
        case HELP: {
            msg.reply("```usage: \n\t #card -n CardName [-i IdolName] [-t CardType]\n\t\t 搜尋卡牌資料\n\t #idol -n IdolName\n\t\t 顯示角色資料\n\t #help\n\t\t 顯示本訊息```");
            break;
        }
        case RAPE: {
            if (msg.content.split(" ").length != 2) {
                msg.channel.send("<:ml_serikapout:663075600503930880>");
                return;
            }

            let kicked = msg.content.split(" ")[1];

            await msg.channel.send("https://cdn.discordapp.com/attachments/474956504475369474/846016218225180743/ezgif.com-gif-maker.gif");
            await msg.channel.send(`:white_check_mark: ${kicked} is raped.`);
            break;
        }
        case KICK: {
            if (msg.content.split(" ").length != 2) {
                msg.channel.send("<:ml_serikapout:663075600503930880>");
                return;
            }

            let kicked = msg.content.split(" ")[1];

            await msg.channel.send("https://tenor.com/view/ayame-hololive-nakiri-ayame-animated-kick-gif-17904529");
            await msg.channel.send(`:white_check_mark: ${kicked} is kicked.`);
            break;
        }
        case PNCH: {
            if (msg.content.split(" ").length != 2) {
                msg.channel.send("<:ml_serikapout:663075600503930880>");
                return;
            }

            let punched = msg.content.split(" ")[1];

            await msg.channel.send("https://64.media.tumblr.com/3fb6fc67715fc67043b2adedac08e87e/ae861ece044bc3a4-4d/s640x960/cff791717756e91dbd6e3fa60e5960d344374ed4.gif");
            await msg.channel.send(`:white_check_mark: ${punched} is punched.`);
            break;
        }
        default:
            //msg.channel.send("<:ml_serikapout:663075600503930880>");
            break;
    }

});
