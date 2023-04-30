print(__name__)
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def drunk():
    print("start drunk water...")
    await asyncio.sleep(5)
    print("wait drunk...")
    await asyncio.sleep(10)
    print("end drunk...")

async def eat():
    print("start eat...")
    await asyncio.sleep(10)
    print("end eat...")

#task = [main(), drunk(), eat()]

async def func1():
    await asyncio.sleep(5)
    print('协程1')

async def func2():
    await asyncio.sleep(5)
    print('协程2')

async def main():

    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
        drunk(),
        eat(),
    )
    
    #task1 = asyncio.create_task(drunk())

    #task2 = asyncio.create_task(eat())

    #await task1
    #await task2

if __name__ == '__main__':
    # python3.7引入的新特性，不用手动创建事件循环
    asyncio.run(main())
