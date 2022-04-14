# meta developer: @Ne_TegayMenya

from telethon import types 
from .. import loader, utils 
from typing import * 
import asyncio 
 
@loader.tds 
class CasinoManMod(loader.Module): 
    'Автоматический казино Saikawa' 
 
    strings = { 
        'name':'SCasinoMan' 
    } 
     
    start: int = 0 
    last: int = 0 
    loses: int = 0 
    is_started: bool = False 
    bot: str = '@SaikawaGame_bot' 
    bot_id: int = 2048687088
     
    async def scasinocmd(self, m: types.Message): 
        '.scasino <x> - начать с x ставки' 
        args: str = utils.get_args_raw(m) 
        if self.is_started: 
            return await utils.answer(m, 'Уже запущен! Для остановки юзай .scasinostop') 
        try: 
            self.last = int(args) 
            self.start = int(args) 
            self.loses = 0 
        except: 
            return await utils.answer(m, 'Введи корректное число') 
        self.is_started = True 
        await m.client.send_message(self.bot, "казино {} ".format(self.start)) 
        await utils.answer(m, 'Запущено! Начальная ставка {}'.format(self.start)) 
 
    async def scasinostopcmd(self, m: types.Message): 
        '.scasinostop - остановить казино' 
        if not self.is_started: 
            return await utils.answer(m, 'Не запущено! Для запуска юзай .scasino <x>') 
        self.is_started = False 
        await utils.answer(m, 'Остановлено!') 
     
    async def watcher(self, m: types.Message): 
        if not isinstance(m, types.Message): 
            return 
        if not hasattr(m.peer_id, 'user_id'): 
            return 
        chat = m.peer_id.user_id 
        if chat == self.bot_id and not m.out and self.is_started: 
            if 'вы выиграли' in m.raw_text: 
                await asyncio.sleep(6) 
                self.loses = 0 
                self.last = self.start 
                await m.client.send_message(self.bot, "казино {} ".format(self.last)) 
            elif 'остаются' in m.raw_text: 
                await asyncio.sleep(6) 
                self.loses = 0 
                await m.client.send_message(self.bot, "казино {} ".format(self.last)) 
            elif 'вы проиграли' in m.raw_text or 'сгорели' in m.raw_text: 
                await asyncio.sleep(6) 
                if self.loses >= 7: 
                    self.loses = 0 
                    self.last = self.start 
                else: 
                    self.last *= 2
                    self.loses += 1 
                await m.client.send_message(self.bot, "казино {} ".format(self.last)) 
            elif 'Недостаточно' in m.raw_text: 
                await asyncio.sleep(6) 
                self.last = self.start 
                self.loses = 0 
                await m.client.send_message(self.bot, "казино {} ".format(self.last))
