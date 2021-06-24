// From https://www.geeksforgeeks.org/program-for-newton-raphson-method/

long double func(long double x)
{
    x = -x;
    return x*x*x - x*x + 2;
}

long double derivFunc(long double x)
{
    return 3*x*x - 2*x;
}

// Function to find the root
long double newton_root()
{
    long double x = 20; // Initial guess
    long double h = func(x) / derivFunc(x);
    for(int i = 0; i < 20; i++)
    {
        h = func(x)/derivFunc(x);
        x = x - h;
    }

    return x;
}
