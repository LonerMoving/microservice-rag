var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient("rag", client =>
{
    client.BaseAddress = new Uri(builder.Configuration["RAG_URL"] ?? "http://localhost:8000");
    client.Timeout = TimeSpan.FromSeconds(120);
});

var app = builder.Build();

app.MapGet("/status", async (IHttpClientFactory factory) =>
{
    var client = factory.CreateClient("rag");
    var response = await client.GetAsync("/status");
    var content = await response.Content.ReadAsStringAsync();
    return Results.Content(content, "application/json");
});

app.MapPost("/index", async (IHttpClientFactory factory) =>
{
    var client = factory.CreateClient("rag");
    var response = await client.PostAsync("/index", null);
    var content = await response.Content.ReadAsStringAsync();
    return Results.Content(content, "application/json");
});

app.MapPost("/ask", async (QuestionRequest request, IHttpClientFactory factory) =>
{
    var client = factory.CreateClient("rag");
    var json = System.Text.Json.JsonSerializer.Serialize(request);
    var body = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
    var response = await client.PostAsync("/ask", body);
    var content = await response.Content.ReadAsStringAsync();
    return Results.Content(content, "application/json");
});

app.Run();

record QuestionRequest(string question);