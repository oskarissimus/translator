const { useState, useEffect } = require("react");

function ErrorBoundary({ children }) {
    const [hasError, setHasError] = useState(false);

    useEffect(() => {
        setHasError(false);
    }, [children]);

    const handleOnError = () => {
        setHasError(true);
    };

    if (hasError) {
        return <div>Something went wrong!</div>;
    }

    return children;
}

function MyComponent() {
    const [items, setItems] = useState(null);

    useEffect(() => {
        fetch("https://jsonplaceholder.typicode.com/todos/1")
            .then((response) => response.json())
            .then((json) => setItems(json))
            .catch(() => setItems([]));
    }, []);

    return (
        <div>
            <h1>My Component</h1>
            <ul>
                {items.map((item) => (
                    <li key={item.id}>{item.title}</li>
                ))}
            </ul>
        </div>
    );
}

function App() {
    return (
        <div>
            <ErrorBoundary>
                <MyComponent />
            </ErrorBoundary>
        </div>
    );
}
