import uvicorn


def main():
    uvicorn.run(
        'webtronics.app:app',
        reload=True
    )


if __name__ == '__main__':
    main()
