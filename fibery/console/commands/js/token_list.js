async () => {
    let response = await fetch(`https://${window.location.host}/api/tokens`, { method: 'GET' });

    if (response.ok) {
        return await response.json();
    }
    return `Error: ${response.status}`;
}
