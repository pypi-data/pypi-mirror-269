//
// Created by Michal Janecek on 27.01.2024.
//

#ifndef WUFF_WOOWOOANALYZER_H
#define WUFF_WOOWOOANALYZER_H


#include <filesystem>
#include <string>
#include <unordered_map>
#include <pybind11/pytypes.h>
#include "document/DialectedWooWooDocument.h"
#include "parser/Parser.h"
#include "dialect/DialectManager.h"
#include "lsp/LSPTypes.h"

class Hoverer;
class Highlighter;
class Navigator;
class Completer;
class Linter;
class Folder;


namespace fs = std::filesystem;
namespace py = pybind11;

class WooWooAnalyzer {
private:
    std::unordered_map<std::string, std::unordered_map<std::string, DialectedWooWooDocument*>> projects;
    std::unordered_map<std::string, std::string> docToProject;
    Parser* parser;
    Hoverer* hoverer;
    Highlighter* highlighter;
    Navigator * navigator;
    Completer * completer;
    Linter * linter;
    Folder * folder;

public:
    WooWooAnalyzer();
    ~WooWooAnalyzer(); 
    void setDialect(const std::string& dialectPath);
    void loadWorkspace(const std::string& workspaceUri);
    DialectedWooWooDocument * getDocumentByUri(const std::string & docUri);
    DialectedWooWooDocument * getDocument(const std::string& pathToDoc);
    DialectManager* dialectManager;
    
    std::vector<DialectedWooWooDocument *> getDocumentsFromTheSameProject(WooWooDocument * document);
    
    // LSP-like functionalities
    std::string hover(const TextDocumentPositionParams &params);
    std::vector<int> semanticTokens(const TextDocumentIdentifier & tdi);
    Location goToDefinition(const DefinitionParams& params);
    std::vector<CompletionItem> complete(const CompletionParams & params);
    std::vector<Location> references(const ReferenceParams & params);
    WorkspaceEdit rename(const RenameParams & params);
    std::vector<Diagnostic> diagnose(const TextDocumentIdentifier & tdi); 
    std::vector<FoldingRange> foldingRanges(const TextDocumentIdentifier & tdi);
    
    // LSP support functions

    void setTokenTypes(std::vector<std::string> tokenTypes);
    void setTokenModifiers (std::vector<std::string> tokenModifiers);
    void documentDidChange(const TextDocumentIdentifier & tdi, std::string &source);
    WorkspaceEdit renameFiles(const std::vector<std::pair<std::string, std::string>> & renames);
    void openDocument(const TextDocumentIdentifier & tdi);
    void didDeleteFiles(const std::vector<std::string> & uris);
    
private:

    std::vector<fs::path> findProjectFolders(const fs::path& rootPath);
    std::optional<fs::path> findProjectFolder(const std::string& uri);
    
    void loadDocument(const fs::path& projectPath, const fs::path& documentPath);
    void deleteDocument(WooWooDocument * document);
    void deleteDocument(const std::string & uri);
    void handleDocumentChange(const TextDocumentIdentifier & tdi, std::string & source);
    static std::vector<fs::path> findAllWooFiles(const fs::path  & rootPath);

    fs::path workspaceRootPath;
};



#endif //WUFF_WOOWOOANALYZER_H
