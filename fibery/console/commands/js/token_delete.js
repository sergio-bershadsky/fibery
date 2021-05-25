async () => {
    let response = await fetch(`https://${window.location.host}/api/tokens/#token_id`, { method: 'DELETE' });

    if (response.ok) {
        return true;
    }
    return `Error: ${response.status}`;
}
