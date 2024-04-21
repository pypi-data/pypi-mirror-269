//
// Created by Michal Janecek on 31.01.2024.
//

#include "Navigator.h"

#include "../utils/utils.h"
#include <algorithm>  // Include for std::find_if

Navigator::Navigator(WooWooAnalyzer *analyzer) : Component(analyzer) {
    prepareQueries();
}

// - - REFERENCES

std::vector<Location> Navigator::references(const ReferenceParams &params) {
    auto document = analyzer->getDocumentByUri(params.textDocument.uri);
    auto pos = document->utfMappings->utf16ToUtf8(params.position.line, params.position.character);
    uint32_t line = pos.first;
    uint32_t character = pos.second;

    TSQueryCursor *cursor = ts_query_cursor_new();
    TSPoint start_point = {line, character};
    TSPoint end_point = {line, character + 1};
    ts_query_cursor_set_point_range(cursor, start_point, end_point);
    ts_query_cursor_exec(cursor, queries[findReferencesQuery], ts_tree_root_node(document->tree));

    TSQueryMatch match;
    std::string nodeType;
    std::string nodeText;
    if (ts_query_cursor_next_match(cursor, &match)) {
        if (match.capture_count > 0) {
            TSNode node = match.captures[0].node;

            nodeType = ts_node_type(node);
            nodeText = document->getNodeText(node);

            if (nodeType == "meta_block") {
                // user executed Find All References on a meta-block
                return findMetaBlockReferences(params);
            }

        }
    }

    return {};

}

std::vector<Location> Navigator::findMetaBlockReferences(const ReferenceParams &params) {
    std::vector<Location> locations;

    auto metaFieldContext = extractMetaFieldKeyValue(params.textDocument, params.position);
    if (metaFieldContext.has_value()) {

        auto document = analyzer->getDocumentByUri(params.textDocument.uri);
        auto mx = metaFieldContext->first;
        auto keyNode = metaFieldContext->second.first;
        auto valueNode = metaFieldContext->second.second;

        auto s = ts_node_start_point(valueNode);
        auto e = ts_node_end_point(valueNode);
        
        auto metaKey = document->getMetaNodeText(mx, keyNode);

        // check if we should include declaration, and if this metaKey is referencable (dialect-specific behaviour)
        if (params.includeDeclaration &&
            std::any_of(analyzer->dialectManager->allReferences.begin(),
                        analyzer->dialectManager->allReferences.end(),
                        [&metaKey](const Reference& ref) { return ref.metaKey == metaKey; })) {

            Location l = {utils::pathToUri(document->documentPath), Range{{s.row + mx->lineOffset, s.column},
                                                                          {e.row + mx->lineOffset, e.column}}};
            document->utfMappings->utf8ToUtf16(l);
            locations.emplace_back(l);
        }

        searchProjectForReferences(locations, document, Reference(metaKey),
                                   document->getMetaNodeText(mx, valueNode));
        return locations;
    } else {
        return {};
    }
}

void
Navigator::searchProjectForReferences(std::vector<Location> &locations, WooWooDocument *doc, const Reference &reference,
                                      const std::string &referenceValue) {

    for (auto projectDocument: analyzer->getDocumentsFromTheSameProject(doc)) {
        for (auto refLocation: projectDocument->findLocationsOfReferences(reference, referenceValue)) {
            projectDocument->utfMappings->utf8ToUtf16(refLocation);
            locations.emplace_back(refLocation);
        }
    }
}

// - - RENAME

WorkspaceEdit Navigator::rename(const RenameParams &params) {

    // First, get all references of the symbol.
    ReferenceParams rp = ReferenceParams(params.textDocument, params.position, true);
    auto referencesLocations = references(rp);

    WorkspaceEdit we;
    for (const auto &refLoc: referencesLocations) {
        TextEdit te = TextEdit(refLoc.range, params.newName);
        we.add_change(refLoc.uri, te);
    }

    return we;
}

// - - GO TO DEFINITION
Location Navigator::goToDefinition(const DefinitionParams &params) {
    auto document = analyzer->getDocumentByUri(params.textDocument.uri);
    auto pos = document->utfMappings->utf16ToUtf8(params.position.line, params.position.character);
    uint32_t line = pos.first;
    uint32_t character = pos.second;

    TSQueryCursor *cursor = ts_query_cursor_new();
    TSPoint start_point = {line, character};
    TSPoint end_point = {line, character + 1};
    ts_query_cursor_set_point_range(cursor, start_point, end_point);
    ts_query_cursor_exec(cursor, queries[goToDefinitionQuery], ts_tree_root_node(document->tree));

    TSQueryMatch match;
    std::string nodeType;
    std::string nodeText;
    if (ts_query_cursor_next_match(cursor, &match)) {
        if (match.capture_count > 0) {
            TSNode node = match.captures[0].node;

            nodeType = ts_node_type(node);
            nodeText = document->getNodeText(node);

            if (nodeType == "filename") {
                return navigateToFile(params, nodeText);
            }
            if (nodeType == "short_inner_environment") {
                return resolveShortInnerEnvironmentReference(params, node);
            }
            if (nodeType == "verbose_inner_environment_hash_end") {
                return resolveShorthandReference("#", params, node);
            }
            if (nodeType == "verbose_inner_environment_at_end") {
                return resolveShorthandReference("@", params, node);
            }
            if (nodeType == "meta_block") {
                return resolveMetaBlockReference(params);
            }

        }
    }
    return Location("", Range{Position{0, 0}, Position{0, 0}});
}

Location Navigator::navigateToFile(const DefinitionParams &params, const std::string &relativeFilePath) {
    auto document = analyzer->getDocumentByUri(params.textDocument.uri);
    auto fileBegin = Range{Position{0, 0}, Position{0, 0}};
    fs::path filePath = fs::canonical(document->documentPath.parent_path() / relativeFilePath);
    auto fileUri = "file://" + filePath.generic_string();
    return {fileUri, fileBegin};
}


Location Navigator::resolveShortInnerEnvironmentReference(const DefinitionParams &params, TSNode node) {
    auto document = analyzer->getDocumentByUri(params.textDocument.uri);
    auto shortInnerEnvironmentType = utils::getChildText(node, "short_inner_environment_type", document);

    // obtain what can be referenced by this environment
    std::vector<Reference> referenceTargets = document->dialectManager->getPossibleReferencesByTypeName(
            shortInnerEnvironmentType);

    // obtain the body part of the referencing environment 
    auto value = utils::getChildText(node, "short_inner_environment_body", document);

    return findReference(params, referenceTargets, value);
}

Location
Navigator::resolveShorthandReference(const std::string &shorthandType, const DefinitionParams &params, TSNode node) {
    auto document = analyzer->getDocumentByUri(params.textDocument.uri);

    // obtain what can be referenced by this environment
    std::vector<Reference> referenceTargets = document->dialectManager->getPossibleReferencesByTypeName(shorthandType);

    return findReference(params, referenceTargets, document->getNodeText(node));
}


std::optional<std::pair<MetaContext *, std::pair<TSNode, TSNode>>>
Navigator::extractMetaFieldKeyValue(const TextDocumentIdentifier &tdi, const Position &p) {
    auto document = analyzer->getDocumentByUri(tdi.uri);
    auto pos = document->utfMappings->utf16ToUtf8(p.line, p.character);
    uint32_t line = pos.first;
    uint32_t character = pos.second;
    TSQueryCursor *cursor = ts_query_cursor_new();
    MetaContext *mx = document->getMetaContextByLine(line);
    // points adjusted by metablock position
    TSPoint start_point = {line - mx->lineOffset, character};
    TSPoint end_point = {line - mx->lineOffset, character + 1};
    ts_query_cursor_set_point_range(cursor, start_point, end_point);
    ts_query_cursor_exec(cursor, queries[metaFieldQuery], ts_tree_root_node(mx->tree));

    TSQueryMatch match;
    while (ts_query_cursor_next_match(cursor, &match)) {
        TSNode metaFieldName;
        TSNode metaFieldValue;
        bool foundValue = false;
        bool foundKey = false;
        for (uint32_t i = 0; i < match.capture_count; ++i) {
            TSNode capturedNode = match.captures[i].node;
            uint32_t capture_id = match.captures[i].index;

            uint32_t capture_name_length;
            const char *capture_name_chars = ts_query_capture_name_for_id(queries[metaFieldQuery], capture_id,
                                                                          &capture_name_length);
            std::string capture_name(capture_name_chars, capture_name_length);
            if (capture_name == "key") {
                foundValue = true;
                metaFieldName = capturedNode;
            } else if (capture_name == "value") {
                foundKey = true;
                metaFieldValue = capturedNode;
            }
        }
        if (foundKey && foundValue) {
            ts_query_cursor_delete(cursor);
            return std::make_pair(mx, std::make_pair(metaFieldName, metaFieldValue));
        }
    }

    ts_query_cursor_delete(cursor);
    return std::nullopt;
}

Location Navigator::resolveMetaBlockReference(const DefinitionParams &params) {
    auto metaFieldContext = extractMetaFieldKeyValue(params.textDocument, params.position);
    if (metaFieldContext.has_value()) {
        auto mx = metaFieldContext->first;
        auto keyNode = metaFieldContext->second.first;
        auto valueNode = metaFieldContext->second.second;
        auto document = analyzer->getDocumentByUri(params.textDocument.uri);
        return findReference(params, document->dialectManager->getPossibleReferencesByTypeName(
                                     document->getMetaNodeText(mx, keyNode)),
                             document->getMetaNodeText(mx, valueNode));
    } else {
        return Location("", Range{Position{0, 0}, Position{0, 0}});

    }
}


Location Navigator::findReference(const DefinitionParams &params, const std::vector<Reference> &possibleReferences,
                                  const std::string &referencingValue) {
    auto document = analyzer->getDocumentByUri(params.textDocument.uri);

    for (auto doc: analyzer->getDocumentsFromTheSameProject(document)) {
        std::optional<std::pair<MetaContext *, TSNode>> foundRef = doc->findReferencable(possibleReferences,
                                                                                         referencingValue);

        if (foundRef.has_value()) {
            MetaContext *mx = foundRef.value().first;
            TSPoint start_point = ts_node_start_point(foundRef.value().second);
            TSPoint end_point = ts_node_end_point(foundRef.value().second);
            auto s = document->utfMappings->utf8ToUtf16(start_point.row + mx->lineOffset, start_point.column);
            auto e = document->utfMappings->utf8ToUtf16(end_point.row + mx->lineOffset, end_point.column);

            auto fieldRange = Range{Position{s.first, s.second}, Position{e.first, e.second}};
            return {utils::pathToUri(doc->documentPath), fieldRange};
        }
    }
    return Location("", Range{Position{0, 0}, Position{0, 0}});
}


// - - - - - - -

WorkspaceEdit Navigator::refactorDocumentReferences(const std::vector<std::pair<std::string, std::string>> & renamedDocuments) {
    WorkspaceEdit we;
    for (const auto &documentRename: renamedDocuments) {
        // document that was renamed (internally, in analyzer, the path should be already updated)
        WooWooDocument *renamedDoc = analyzer->getDocument(documentRename.second);
        std::string oldFileName = documentRename.first;
        fs::path oldFilePath(oldFileName);
        fs::path oldFileDir = oldFilePath.parent_path();
        
        // iterate over every document from the same project and look for references (from include statements)
        for (WooWooDocument *projectDocument: analyzer->getDocumentsFromTheSameProject(renamedDoc)) {
            TSQueryCursor *cursor = ts_query_cursor_new();
            ts_query_cursor_exec(cursor, queries[filenameQuery], ts_tree_root_node(projectDocument->tree));
            TSQueryMatch match;
            std::string nodeType;
            std::string nodeText;
            
            while (ts_query_cursor_next_match(cursor, &match)) {
                if (match.capture_count > 0) {
                    TSNode node = match.captures[0].node;
                    nodeText = projectDocument->getNodeText(node);

                    fs::path includedFilePath(nodeText);
                    if (!includedFilePath.is_absolute()) {
                        includedFilePath = projectDocument->documentPath.parent_path() / includedFilePath;
                    }

                    try {
                        if(fs::canonical(oldFilePath) == fs::canonical(includedFilePath)){
                            // found include referring to the old filename
                            // we want to replace it with the new filename
                            
                            fs::path relativePath = fs::relative(renamedDoc->documentPath, projectDocument->documentPath.parent_path());

                            auto s = ts_node_start_point(node);
                            auto e = ts_node_end_point(node);

                            Location l = {utils::pathToUri(projectDocument->documentPath), Range{{s.row, s.column},
                                                                                              {e.row, e.column}}};
                            projectDocument->utfMappings->utf8ToUtf16(l);
                            
                            TextEdit te = TextEdit(l.range, relativePath.generic_string());
                            we.add_change(l.uri, te);
                        }

                    } catch (...) {
                        // if something fails, simply do not refactor it
                    }
                }
            }
        }
    }
    return we;
}

// - - - - - - -

const std::unordered_map<std::string, std::pair<TSLanguage *, std::string>> &Navigator::getQueryStringByName() const {
    return queryStringsByName;
}

const std::string Navigator::metaFieldQuery = "metaFieldQuery";
const std::string Navigator::goToDefinitionQuery = "goToDefinitionQuery";
const std::string Navigator::findReferencesQuery = "findReferencesQuery";
const std::string Navigator::filenameQuery = "filenameQuery";
const std::unordered_map<std::string, std::pair<TSLanguage *, std::string>> Navigator::queryStringsByName = {
        {metaFieldQuery,      std::make_pair(tree_sitter_yaml(), MetaContext::metaFieldQueryString)},
        {goToDefinitionQuery, std::make_pair(tree_sitter_woowoo(),
                                             R"(
(filename) @type
(short_inner_environment) @type
(verbose_inner_environment_hash_end) @type
(verbose_inner_environment_at_end) @type
(meta_block) @type
)")},
        {findReferencesQuery, std::make_pair(tree_sitter_woowoo(),
                                             R"(
(meta_block) @type
)")},
        {filenameQuery,       std::make_pair(tree_sitter_woowoo(), "(filename) @filename")}
};


