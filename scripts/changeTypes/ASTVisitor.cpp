// This file is adapted from Joao Rivera

/* Clang front end header files */
#include "clang/Driver/Options.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/ASTConsumers.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "clang/Rewrite/Core/Rewriter.h"

#include <sstream>
#include <fstream>
#include <map>

/* Other headers */
#include <iostream>
#include "vector"
#include "ASTVisitor.h"
#include "ASTTraverser.h"

using namespace std;
using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace llvm;

Rewriter rewriter;
CompilerInstance* mainCI;
int numFunctions = 0;

map<string, string> vars;

string argTypes = "";



/* Apply a custom category to all command-line options so that they are the only ones displayed. */
llvm::cl::OptionCategory MyToolCategory("my-tool options");

string getRawCodeAsString(SourceRange sr) {
    return rewriter.getRewrittenText(sr);
}

class NodeTraverser : public ASTTraverser {
    friend ASTTraverser;

    void ActionBinaryOperator(clang::BinaryOperator* bop) {
        if(bop->isAssignmentOp() && bop->getType()->isFloatingType()) {
            outs() << "Assignment detected\n";
            //bop->dump(); /* Print AST of this node */
            outs() << getRawCodeAsString(bop->getSourceRange()) << "\n";
        }
    }

public:
    template<typename T>
    explicit NodeTraverser(T* st) {
        _traverseAST(st);
    }
};

class ASTMainVisitor : public RecursiveASTVisitor<ASTMainVisitor> {
    friend RecursiveASTVisitor<ASTMainVisitor>;

    /* Context used for getting additional AST info */
    ASTContext* astMainContext;
    SourceLocation processedLocation;

    bool ActionFunctionDecl(FunctionDecl *fund) {
        numFunctions++;
        string funcName = fund->getNameAsString();

        if (fund->doesThisDeclarationHaveABody()) {
//            /* Traverse AST below this node */
//            Stmt* body = fund->getBody();
//            NodeTraverser n(body);
        }


        int numArgs = fund->getNumParams();

        for(int i = 0; i < numArgs; i++){
          string argName = fund->parameters()[i]->getNameAsString();
          string orig_type = fund->parameters()[i]->getType().getAsString();
          string funName = fund->getNameAsString();
          auto it = vars.find(funName + "#" + argName);
          if(it != vars.end()){
              string type = it->second;
              argTypes += funName + ", " + argName + ", " + type + "\n";
          }

        }

        return true;
    }

    bool ActionVarDecl(VarDecl *var) {
        SourceRange varLocRange = var->getSourceRange();

        //if(!var->getType()->isRealFloatingType()) {
            /* Return if it is not floating point. This does not support pointers, e.g. double*. */
        //    return true;
        //}

        string orig_type = var->getType().getAsString();
        string varName = var->getNameAsString();
        string funName = ((FunctionDecl*)var->getParentFunctionOrMethod())->getNameAsString();



        auto it = vars.find(funName + "#" + varName);
        if(it != vars.end()){
            string type = it->second;
            //if(orig_type == "long double *"){ // just for now
            //  goto end;
            //}
            //cout << type << " \n";
            SourceRange typeRange = var->getTypeSourceInfo()->getTypeLoc().getSourceRange();
            rewriter.ReplaceText(typeRange, type);
        }
        //end:
        /* To handle same-line-declarations, test that begin location is not already processed */
        //if (processedLocation < varLocRange.getBegin()) {

        //}

        processedLocation = varLocRange.getEnd();
        return true;
    }

    /* There are two main parent classes in the clang AST, namely Stmt and Decl. Most of the nodes
     * are derived from them. An exception is AttributedStmt. This node is not caught by VisitStmt. */
    bool VisitStmt(Stmt *st) {

        /* Check that the statement is in the main file. If not, it is most likely in a header file*/
        SourceManager& SM = rewriter.getSourceMgr();
        if (!SM.isInMainFile(st->getBeginLoc())) {
            /* The current location is not in the main file. Do not process.
             * (It is most likely in a header file.) */
            return true;
        }

        /* Process expression, e.g. binary expression, function calls, etc */
        if (auto *expr  = dyn_cast<Expr>(st)) {
            return true;
        }

        /* Process if-else statement */
        if (auto *ifs = dyn_cast<IfStmt>(st)) {
            return true;
        }

        /* Process while-loop conditions */
        if (auto *whs = dyn_cast<WhileStmt>(st)) {
            return true;
        }

        /* Process for-loop */
        if (auto *frs = dyn_cast<ForStmt>(st)) {
            return true;
        }

        /* Process do-while */
        if (auto *dws = dyn_cast<DoStmt>(st)) {
            return true;
        }

        /* Process return statement */
        if (auto *res = dyn_cast<ReturnStmt>(st)) {
            return true;
        }
        return true;
    }

    bool VisitDecl(Decl* decl) {
        SourceManager& SM = rewriter.getSourceMgr();
        if (!SM.isInMainFile(decl->getLocation())) {
            /* The current location is not in the main file. Do not process.
             * (It is most likely in a header file.) */
            return true;
        }

        if (auto *fund = dyn_cast<FunctionDecl>(decl)) {
            return ActionFunctionDecl(fund);
        }

        if (auto *fld = dyn_cast<FieldDecl>(decl)) {
            return true;
        }

        if (auto *var = dyn_cast<VarDecl>(decl)) {
            return ActionVarDecl(var);
        }

        if (auto *tyd = dyn_cast<TypedefDecl>(decl)) {
            return true;
        }

        return true;
    }

public:
    explicit ASTMainVisitor(CompilerInstance *CI) : astMainContext(&(CI->getASTContext())) {
        mainCI = CI;
        rewriter.setSourceMgr(astMainContext->getSourceManager(), astMainContext->getLangOpts());
    }
};

class ExampleASTConsumer : public ASTConsumer {
private:
    ASTMainVisitor *visitor; // doesn't have to be private

public:
    /* Override the constructor in order to pass CI */
    explicit ExampleASTConsumer(CompilerInstance *CI)
            : visitor(new ASTMainVisitor(CI)) // initialize the visitor
    { }

    /* Override this to call our ASTMainVisitor on the entire source file */
    void HandleTranslationUnit(ASTContext &Context) override {
        /* ASTContext is used to get the TranslationUnitDecl (a declaration representing the entire source file). */
        TranslationUnitDecl* tud = Context.getTranslationUnitDecl();

        /* Now traverse the entire main visitor to perform the interval transformations */
        visitor->TraverseDecl(tud);
    }
};

class ExampleFrontendAction : public ASTFrontendAction {
public:
    ExampleFrontendAction() = default;

    void EndSourceFileAction() override {
        /* Do something when end of source is reached */
    }

    virtual std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI, StringRef file) override {
        return (std::unique_ptr<ASTConsumer>) new ExampleASTConsumer(&CI); // pass CI pointer to ASTConsumer
    }
};

int main(int argc, const char **argv) {
    // read config from config files
    std::ifstream t("config_temp.json");
    std::stringstream buffer;
    buffer << t.rdbuf();
    string line;
    argTypes = "";
    string funname = "";
    string type = "";
    string varname = "";

    while(getline(buffer, line)){
      if (line.find("function") != string::npos) {
        auto pos = line.find(": \"") + 3;
        while(line[pos] != '\"'){
          funname += line[pos];
          pos++;
        }
      }
      if (line.find("type") != string::npos) {
        auto pos = line.find(": \"") + 3;
        while(line[pos] != '\"'){
          type += line[pos];
          pos++;
        }
        if(type == "longdouble"){
          type = "long double";
        }else if(type == "longdouble*"){
          type = "long double *";
        }
      }
      if (line.find("name") != string::npos) {
        auto pos = line.find(": \"") + 3;
        while(line[pos] != '\"'){
          varname += line[pos];
          pos++;
        }
      }

      if (line.find("call") != string::npos){
        getline(buffer, line);
        getline(buffer, line);
        getline(buffer, line);
        getline(buffer, line);
        getline(buffer, line);
        funname = "";
        type = "";
        varname = "";
      }

      if(funname != "" && type != "" && varname != ""){
        vars.insert(make_pair(funname + "#" + varname, type));
        funname = "";
        type = "";
        varname = "";
      }
    }

    /*for(auto iter = vars.begin(); iter != vars.end(); ++iter)
    {
      auto k = iter->first;
      auto v = iter->second;
      cout << k << " " << v << "\n";
    }*/

    CommonOptionsParser op(argc, argv, MyToolCategory);

    /* create a new Clang Tool instance (a LibTooling environment) */
    ClangTool Tool(op.getCompilations(), op.getSourcePathList());

    /* run the Clang Tool, creating a new FrontendAction */
    int result = Tool.run(newFrontendActionFactory<ExampleFrontendAction>().get());

    /* print out the rewritten source code */
    //errs() << "\nFound " << numFunctions << " functions.\n\n";
    FileID fid = rewriter.getSourceMgr().getMainFileID();
    rewriter.getEditBuffer(fid).write(outs());

    // write arg types to file
    ofstream myfile ("funargs.txt");
    myfile << argTypes;
    myfile.close();

    return result;
}
